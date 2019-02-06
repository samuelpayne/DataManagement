from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from . import forms
import re
from Records.models import Sample, Dataset, Experiment
from django.forms.models import model_to_dict
from django_tables2 import RequestConfig
from Records.tables import SampleTable, DatasetTable, ExperimentTable
from datetime import datetime
from django.forms import formset_factory
# Create your views here.

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

def upload(request):
	form = forms.UploadFileForm()
	if request.method == 'POST':
		form = forms.UploadFileForm(request.POST, request.FILES)
		return excel.make_response(filehandle.get_sheet(), "csv",
			file_name="download")
	context = {
		'form':form
	}
	return render(request, 'upload.html',context)


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
        if form.is_valid():
            new_Dataset = form.save(commit = False)
            new_Dataset._experiment = new_Dataset.sample().experiment()
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
	

def add_instrument(request):
	form = forms.InstrumentForm()
	if request.method == 'POST':
		form = forms.InstrumentForm(request.POST)
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
		form = forms.InstrumentSettingForm(request.POST)
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
		form = forms.ProtocolForm(request.POST)
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
		form = forms.fileStatusOptionForm(request.POST)
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
		form = forms.ExperimentalDesignForm(request.POST)
		if form.is_valid():
			new_inst = form.save()
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
            dataset._experiment = dataset.sample().experiment()
            dataset.save()
            return redirect('datasets')
    
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
                return redirect('samples')
    
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
            return redirect('experiments')
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

"""class PatientView(ListView):
    model = Patient
    queryset = Patient.objects.all()
    template_name = 'patient_list.html'
    paginate_by = 25
    #"""

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

