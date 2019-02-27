"""This is the code handling each of the pages."""

from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from . import forms
import re
from Records.models import *
from django.forms.models import model_to_dict
from django_tables2 import RequestConfig
from Records.tables import *
from Records.read_maps import *
from datetime import datetime
from django.forms import formset_factory
import openpyxl

"""Records named 'records'
    Give options:
     -view Archives
     -add records"""
def records(request):
    return render(request, 'records.html')

def about(request):
    return render(request, 'about.html')

"""Archive home named 'archive'
    Allow type selection"""
def archive(request):
    #get the url parameter for what type of data to display, if any
    param = re.sub('/records/archive/','',request.get_full_path())
    param = re.sub('\?type=','',param)
    if param == 'experiments' :
        model = Experiment
    elif param == 'samples':
        model = Sample
    elif param == 'datasets':
        model = Dataset
    else:
        model = None
    if model is not None:
        query_results = model.objects.all()
        results = [model_to_dict(r) for r in query_results]
        col_names = [re.sub(r'\w+\.\w+\.', '', str(i)) for i in model._meta.get_fields()]
        col_names = col_names[1:]  #using the [1:] so it skips the first item which just declares it is one to many or one to one
        fields = [model._meta.get_field(i).verbose_name for i in col_names]
    else:
        results = []
        col_names = []
        fields = []
    data = {
    'type' : param,
    'show_table': param not in ['experiments','samples','datasets'],
    'query_results': results,
    'col_names': fields,
    }
    """or:
    for type in RecordTypes:
        data[type] = type.objects.all().count()
        #or whatever you want this page to know"""
    return render(request, 'archive.html', context = data)

def create_new(request):
    return render(request, 'create-new.html',)

def success(request):
	return render(request, 'success.html')
	
def upload(request):
	form = forms.UploadFileForm()
	upload_status = ['']
	summary = ''
	if request.method == 'POST':
		print ("Hello\n\n\n\n")
		form = forms.UploadFileForm(request.POST, request.FILES)
		print ("Form Validity check:", form.is_valid())
		if form.is_valid():
			file = request.FILES['_File']
			data = form.save(commit = False)
			lead = data.lead
			#print (file)
		#try: #Catch invalid formats, etc.
		if True: #Allows for effective debugging
			print ("Trying open...")
			wb = openpyxl.load_workbook(file, data_only=True)
			#read_only = True sometimes causes sharing violations 
			#because it doesn't close fully
			print ("Successful open")
			if wb['Input']['I3'].value == "Mass spec":
				upload_status = read_data(wb, lead, read_in_map_MS) #to be used in template
			elif wb['Input']['I3'].value == "Instrument Type":
				
				upload_status = read_data(wb, lead, read_in_map_gen)#"Upload Successful"
			else: 
				print('Unknown format')
				upload_status = "Unknown format. Please use one of the provided templates."
			wb.close()
		"""except:
			print("Read in error") 
			upload_status = "Read in error.\nPlease use one of the provided templates."
		#"""
		#return redirect('records')
		if len(upload_status) >1: summary = upload_status[1:]

	context = {
		'form':form,
		'upload_status':upload_status[0],
		'summary': summary,
	}
	return render(request, 'upload.html',context)

NEW = 'NEW'
EXISTING = '(Existing)'
def read_data(wb, lead, read_map):
	wsIn = wb[read_map['wsIn']]
	if wsIn[read_map['start_loc']].value is None:
		print ("Empty file")
		return ["Empty file"]

	summary = [("Upload summary:")]
	wlrowNum = read_map['wlrowNumInit']
	for i in wsIn[(read_map['in_section']).format(wsIn.max_row)]:
		#each record a dataset associated with a sample
		if i[read_map['sample_name']].value is None:
			return summary
			#All done!
		wlrowNum +=1
		wlRow = wb[read_map['wsWL']][wlrowNum]

		#Otherwise read it in
		e_n = exp_exist_or_new(i[read_map['experiment_loc']].value, lead)
		experiment = e_n[2]
		summary.append(e_n)

		e_n = sample_exists_or_new(i[read_map['sample_name']].value, experiment, i, wsIn, read_map)
		sample = e_n[2]
		summary.append(e_n)
		
		e_n = dataset_exists_or_new(wlRow[read_map['dataset_name']].value, experiment, sample, i, wb, wsIn, wlRow, read_map)
		summary.append(e_n)

		print (summary)

	wlRow = None
	wsIn = None

#overload for additional information
def exp_exist_or_new(name, lead):
	experiments = Experiment.objects.all()
	if experiments.filter(_experimentName = name).exists():
		return [EXISTING, 'Experiment: ', experiments.get(_experimentName = name)]
	#the experiment needs to be created
	newExp = Experiment(
		_experimentName = name,
		_projectLead =  lead,
	)
	newExp.save()
	return [NEW, 'Experiment: ', newExp]

def sample_exists_or_new(name, experiment, row, wsIn, read_map):
	samples = Sample.objects.all()
	if samples.filter(_sampleName = name).exists():
		return [EXISTING, 'Sample: ', samples.get(_sampleName = name)]

	comment = ""
	for c in read_map['comments_row']:
		comment += c
		comment += str(row[read_map['comments_row'][c]].value)+'\n'
	for c in read_map['comments_gen']:
		comment += c
		comment += str(wsIn[read_map['comments_gen'][c]].value)+'\n'

	if read_map['date_global']: date = wsIn[read_map['date_created']].value
	else: date = row[read_map['date_created']].value

	newSample = Sample(
		_sampleName = name,
		_storageCondition = "Processing",
		_experiment = experiment,
		_storageLocation = str(row[read_map['storage_location']].value),
		_dateCreated = datetime.strptime(date, '%M-%d-%Y').strftime('%Y-%m-%d'),
		_organism = wsIn[read_map['organism']].value,
		_comments = comment,
	)
	newSample.save()
	return [NEW, 'Sample: ', newSample]

def dataset_exists_or_new(name, experiment, sample, row, wb, wsIn, wlRow, read_map):
	datasets = Dataset.objects.all()

	if datasets.filter(_datasetName = name).exists():
		return [EXISTING, 'Dataset: ', datasets.get(_datasetName = name)]
		

	def inst_exists_or_new(insName):
		if Instrument.objects.all().filter(_name = insName).exists():
			return [EXISTING,'Instrument: ', Instrument.objects.all().get(_name = insName)]
		ins = Instrument(_name = insName)
		ins.save()
		return [NEW, 'Instrument: ', ins]
	def setting_exists_or_new(methodName):
		if InstrumentSetting.objects.all().filter(_name = methodName).exists():
			return [EXISTING,'Instrument Setting: ',InstrumentSetting.objects.all().get(_name = methodName)]
		ins = InstrumentSetting(_name = methodName)
		settings_column = wb[read_map['settings_sheet']][read_map['settings_keyword_column']]

		filename = wlRow[read_map['settings_file']]
		print(filename)
		try: ins.file = open(filename)
		except: print (filename, " open failed.")
		print ("Settings Saved")
		ins.save()
		return [NEW, 'Instrument Setting: ', ins]

	summary = []
	e_n = inst_exists_or_new((wsIn[read_map['instrument_type_loc']].value+' '+wsIn[ read_map['inst_code']].value))
	initInstrument = e_n[2]
	if (e_n[0] == NEW): summary.append(e_n)
	e_n = setting_exists_or_new(row[read_map['setting_loc']].value)
	setting = e_n[2]

	dataType = wsIn[read_map['data_type_loc']].value
	date = datetime.strptime(wsIn[read_map['date_loc']].value, '%M-%d-%Y').strftime('%Y-%m-%d')

	if read_map['file_extension_from_excel']: extension = str(wsWL[read_map['file_extension']].value)
	else: extension = str(read_map['file_extension'])

	wsWL = wb[read_map['wsWL']]
	newDataset = Dataset(
		_datasetName = name,
		_experiment = experiment,
		_instrument = initInstrument,
		_fileName = str(wlRow[read_map['file_name']].value)+extension,
		_fileLocation = str(wlRow[read_map['file_location']].value),
		_instrumentSetting = setting,
		_type = dataType,
		_dateCreated = date,
		#Commas after each value
		#acquisition dates
		#_status
		#_size
		#_fileHash
	)
	newDataset.save()
	newDataset._sample.add(sample)


	return [NEW, 'Dataset: ', newDataset]

"""Page to add a sample"""
def add_sample(request):
    #check anything you want checked
    form =forms.AddSampleForm()
    if request.method == 'POST':
        form =forms.AddSampleForm(request.POST)
        if form.is_valid():
            new_Sample = form.save()
            return redirect('samples')
    buttons = {
        'New Protocol': 'add-protocol',
    }
    context = {
        'form':form,
        'header':'Add Sample',
        'buttons':buttons
    }

    return render(request, 'add-record.html', context)

##"""I'm looking into using a formset for bulk entry"""
def add_sample_bulk(request):
    formset =formset_factory(forms.AddSampleForm())
    if request.method == 'POST':
        formset =formset_factory(forms.AddSampleForm(request.POST, request.FILES))
        """for form in formset:
            if form.is_valid():
                new_Sample = form.save()"""
        return redirect('samples')

    context = {
        'form':form,
        'header':'Add Sample'
    }

    return render(request, 'add-record-bulk.html', context)

def add_dataset(request):
    form =forms.AddDatasetForm()
    if request.method == 'POST':
        form =forms.AddDatasetForm(request.POST)
        print ("Testing Validity")
        if form.is_valid():
            print ("Valid")
            #new_Dataset = form.save(commit = False)
            #new_Dataset._experiment = new_Dataset.sample()[0].experiment()
            new_Dataset = form.save()
            return redirect('datasets')
    buttons = {
        'New Instrument': 'add-instrument',
        'New Instrument Setting': 'add-instrument-setting'
    }
    context = {
        'form':form,
        'header':'Add Dataset',
        'buttons':buttons
    }


    return render(request, 'add-record.html', context)

def add_experiment(request):
    form = forms.AddExperimentForm()
    if request.method == 'POST':
        form =forms.AddExperimentForm(request.POST)
        if form.is_valid():
            new_Experiment = form.save()
            return redirect('experiments')
    buttons = {
        'New Experimental Design': 'add-experimental-design',
    }
    context = {
        'form':form,
        'header':'Add Experiment',
        'buttons':buttons
    }

    return render(request, 'add-record.html', context)

def add_individual(request):
    extra = []#'Gender','Age','Disease Status',]
    form = forms.AddIndividualForm(extraFields = extra)
    if request.method == 'POST':
        form = forms.AddIndividualForm(request.POST, extraFields = extra)
        if form.is_valid():
            new_Individual = form.save(commit = False)
            #parses to JSON
            extraFieldData = '{'
            for f in extra:
                extraFieldData+=' "'+str(f)+'":"'
                extraFieldData += str(form.data[f])+'",'
            extraFieldData +='}'
            new_Individual.setComments(extraFieldData)
            new_Individual.save()
            return redirect('individuals')
    context = {
        'form':form,
        'header':'Add Individual',
    }

    return render(request, 'add-record.html', context)
	

def add_instrument(request):
	form = forms.InstrumentForm()
	if request.method == 'POST':
		form = forms.InstrumentForm(request.POST, request.FILES)
		if form.is_valid():
			new_inst = form.save()
			return redirect('add-dataset')
	context = {
		'form':form,
		'header':'Add Instrument'
	}
	return render(request, 'add-record.html', context)
def add_instrument_setting(request):
	form = forms.InstrumentSettingForm()
	if request.method == 'POST':
		form = forms.InstrumentSettingForm(request.POST, request.FILES)
		if form.is_valid():
			new_inst = form.save()
			return redirect('add-dataset')
	context = {
		'form':form,
		'header':'Add Instrument Setting'
	}
	return render(request, 'add-record.html', context)
def add_protocol(request):
	form = forms.ProtocolForm()
	if request.method == 'POST':
		form = forms.ProtocolForm(request.POST, request.FILES)
		if form.is_valid():
			new_inst = form.save()
			return redirect('add-sample')
	context = {
		'form':form,
		'header':'Add Protocol'
	}
	return render(request, 'add-record.html', context)
def add_file_status(request):
	form = forms.fileStatusOptionForm()
	if request.method == 'POST':
		form = forms.fileStatusOptionForm(request.POST, request.FILES)
		if form.is_valid():
			new_inst = form.save()
			return redirect('add-dataset')
	context = {
		'form':form,
		'header':'Add File Status'
	}
	return render(request, 'add-record.html', context)
def add_experimental_design(request):
	form = forms.ExperimentalDesignForm()
	if request.method == 'POST':
		form = forms.ExperimentalDesignForm(request.POST, request.FILES)
		if form.is_valid():
			newDes = form.save()
			return redirect('add-experiment')
	context = {
		'form':form,
		'header':'Add Experimental Design'
	}
	return render(request, 'add-record.html', context)


def edit_dataset(request, pk):
    dataset = Dataset.objects.get(pk=pk or None)
    form = forms.AddDatasetForm(instance = dataset)
    if request.method == 'POST':
        form =forms.AddDatasetForm(request.POST, instance = dataset)
        if form.is_valid():
            dataset = form.save(commit = False)
            dataset._experiment = dataset.sample()[0].experiment()
            dataset.save()
            return redirect('success')
    
    buttons = {
        'New Instrument':'add-instrument',
        'New Instrument Setting':'add-instrument-setting'
    }
    context = {
        'form':form,
        'header':'Edit Dataset',
        'dataset':dataset,
		'buttons':buttons
    }

    return render(request, 'add-record.html', context)

def edit_sample(request, pk):
    sample = Sample.objects.get(pk=pk)
    form = forms.AddSampleForm(instance = sample)
    if request.method == 'POST':
        form =forms.AddSampleForm(request.POST, instance = sample)
        if form.is_valid():
            sample = form.save()
            #updates dataset key to experiment as well
            try:
                if sample.dataset:
                    sample.dataset._experiment = sample.experiment()
                    sample.dataset.save()
            except:
                DoesNotExist = null #Does nothing but make it not crash
				#something needs to be here, doesn't matter what
            finally:
                return redirect('success')
    
    buttons = {
        'New Protocol':'add-protocol',
    }
    context = {
        'form':form,
        'header':'Edit Sample',
        'sample':sample,
		'buttons':buttons
    }

    return render(request, 'add-record.html', context)

def edit_experiment(request, pk):
    experiment = Experiment.objects.get(pk=pk)
    form = forms.AddExperimentForm(instance = experiment)
    if request.method == 'POST':
        form =forms.AddExperimentForm(request.POST, instance = experiment)
        if form.is_valid():
            experiment = form.save()
            return redirect('success')
    buttons = {
        'New Experimental Design':'add-experimental-design',
    }
    context = {
        'form':form,
        'header':'Edit Experiment',
        'experiment':experiment,
		'buttons':buttons
    }

    return render(request, 'add-record.html', context)



"""(type)Views generate the list view pages
i.e., the list of samples that's now a table"""
class SampleView(ListView):
    model = Sample
    queryset = Sample.objects.all()

    #DataMan\Records\templates\Records\samples_list.html
    template_name = 'samples_list.html'
    context_object_name = 'sample'
    def get_context_data(self, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)
        table = SampleTable(Sample.objects.all().order_by('-pk'))
        RequestConfig(self.request, paginate={'per_page': 25}).configure(table)
        context['table'] = table
        context['Title'] = 'Sample'
        return context

class DatasetView(ListView):
    model = Dataset
    queryset = Dataset.objects.all()
    template_name = 'dataset_list.html'
    context_object_name = 'dataset'
    def get_context_data(self, **kwargs):
        context = super(DatasetView, self).get_context_data(**kwargs)
        table = DatasetTable(Dataset.objects.all().order_by('-pk'))
        RequestConfig(self.request, paginate={'per_page': 25}).configure(table)
        context['table'] = table
        context['Title'] = 'Dataset'
        return context

class ExperimentView(ListView):
    model = Experiment
    queryset = Experiment.objects.all()
    template_name = 'experiment_list.html'
    context_object_name = 'experiment'
    def get_context_data(self, **kwargs):
        context = super(ExperimentView, self).get_context_data(**kwargs)
        table = ExperimentTable(Experiment.objects.all().order_by('-_experimentName'))
        RequestConfig(self.request, paginate={'per_page': 25}).configure(table)
        context['table'] = table
        context['Title'] = 'Experiment'
        return context

class IndividualView(ListView):
    model = Individual
    queryset = Individual.objects.all()
    template_name = 'individual_list.html'
    paginate_by = 25
    def get_context_data(self, **kwargs):
        context = super(IndividualView, self).get_context_data(**kwargs)
        table = IndividualTable(Individual.objects.all().order_by('_individualIdentifier'))
        RequestConfig(self.request, paginate={'per_page': 25}).configure(table)
        context['table'] = table
        context['Title'] = 'Individuals'
        return context

class InstrumentView(ListView):
	model = Instrument
	template_name = 'instrument_list.html'
	paginate_by = 25
	def get_context_data(self, **kwargs):
		context = super(InstrumentView, self).get_context_data(**kwargs)
		RequestConfig(self.request, paginate={'per_page': 25})
		context['Title'] = 'Instruments'
		return context

"""named (type)-detail, these are the detail view
pages generated for the specific record
Ex: sample 1234, dataset 3"""
class SampleDetailView(DetailView):
    model = Sample
    template = 'sample_detail.html'
    #"""

class DatasetDetailView(DetailView):
    instrumentSetting = "new"
    model = Dataset
    template = 'dataset_detail.html'

class ExperimentDetailView(DetailView):
    model = Experiment
    template = 'experiment_detail.html'

class IndividualDetailView(DetailView):
	model = Individual
	template = 'individual_detail.html'