"""Project DataMan

This is the code handling each of the pages.
    It connects the templates to the urls and 
    the information from the database."""

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
from openpyxl.utils import get_column_letter
import json
from os.path import basename
from django.conf import settings
import dropbox
from django.core.management import call_command

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
job = None


NEW = 'NEW'
EXISTING = '(Existing)'

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

def success(request, message = 'Successfully recorded'):
	if request.session.get('message') and request.session['message'] != None:
		message = request.session['message']
	context = {'message':message}
	request.session['message'] = None
	return render(request, 'success.html', context)

def make_backup():
	#print ("Tick, making backup.")

	filename = 'dump-' +datetime.today().strftime('%Y-%m-%d')+'.json'
	#creates local backup
	if settings.BACKUP_LOCATION:
		filepath = settings.BACKUP_LOCATION + filename
	with open(filepath, 'w') as file:
		call_command('dumpdata', 'Records', stdout=file)

	#backs up to box
	if settings.DROPBOX_ACCESS_TOKEN:
		# The full path to upload the file to, including the file name
		box_file = settings.DROPBOX_BACKUP_LOCATION + filename
		##Not yet the right access token...
		dbx = dropbox.Dropbox(settings.DROPBOX_ACCESS_TOKEN)
		with open(filepath, 'rb') as file:
			dbx.files_upload(file.read(), box_file)
	
		link = d.sharing_create_shared_link(targetfile)
		url = link.url
		dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
		print ("\n\n\n",link,'\n',url,'\n',dl_url,'\n')

	return True

def start_job():
	global job

	#Checks if the job has already been assigned so as to avoid duplicates
	if not 'make_backup_job' in str(scheduler.get_jobs()):
		job = scheduler.add_job(make_backup, 'interval', hours = 1, id = 'make_backup_job')
	if not scheduler.running: scheduler.start()

def backup(request):
	start_job()
	options = {'Restore',}
	form = forms.BackUpSelectForm()
	context = {
		'header': 'Backup Options',
		'options':options,
		'form':form
	}
	if request.method == 'POST' and request.POST.get('option') == 'Restore':
		form = forms.BackUpSelectForm(request.POST)
		if form.is_valid():
			data = form.save(commit = False)
			filename = 'dump-' +data.date.strftime('%Y-%m-%d')+'.json'
			filename = settings.BACKUP_LOCATION + filename
			#backupfile = BackupFile.objects.all().get(date = data.date)
			#filename = backupfile.filename()
			try:
				restore(filename)
			except:
				context['error'] = 'No backup was found for that date.'
		else: context['error'] = 'No backup available for that date.'
	
	if request.method == 'GET' and request.GET.get('option') == 'backup-now':
		make_backup()
		return redirect('backup')
	return render(request, 'backup.html', context)

def restore(filename):
	call_command('loaddata', filename, app_label='Records') 

#this method handles the upload page and
#directs the sheet to the read-in method
def upload(request, option = None):
	form = forms.UploadFileForm()
	upload_status = ''
	summary = ''
	upload_summary = ['']
	upload_options = {}

	#print("\n\n\nUpload Page")

	if request.method == 'POST' and request.POST.get('Submit') == 'Submit':
		
		print ("\nAttempting Upload")
		form = forms.UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['_File']
			data = form.save(commit = False)
			lead = data.lead
		#try: #Catch invalid formats, etc.
		if True: #Allows for effective debugging
			wb = openpyxl.load_workbook(file, data_only=True)
			#read_only = True sometimes causes sharing violations 
			#because it doesn't close fully
			if wb['Input']['I3'].value == "Mass spec":
				upload_summary = read_data(request, wb, lead, read_in_map_MS) #to be used in template
				request.session['upload_summary']
				read_map = read_in_map_MS
			elif wb['Input']['I3'].value == "Instrument Type":
				upload_summary = read_data(request, wb, lead, read_in_map_gen)#"Upload Successful"
				read_map = read_in_map_gen
			else: 
				upload_summary = "Unknown format. Please use one of the provided templates."
			wb.close()
			upload_options = {
				'Confirm': True,
				'Cancel': False,
			}
			request.session['upload_status'] = upload_status
		#except:
		#	upload_status = "Read in error.\nPlease use one of the provided templates."
		#print("finished Upload")
		#"""

		#saves summary of changes till delete option
		i = 0 
		request.session['upload_summary'] = {}
		for report in upload_summary:
			request.session['upload_summary'][i] = report
			i +=1
		request.session.modified = True
		
		print("read in complete")
		if 'missing_fields' in request.session:
			del request.session['missing_fields']
		if 'missing_fields_data' in request.session:
			del request.session['missing_fields_data']
		missing_fields= get_missing_fields(wb, read_map)
		missing_fields = list(dict.fromkeys(missing_fields))
		print ('missing_fields: ', missing_fields)
		
		request.session['missing_fields'] = missing_fields
		return redirect ('process_missing_fields')

	context = {
		'form':form,
		'upload_status':upload_status,
		'summary': summary,
		'upload_options': upload_options,
	}

	#Cancel options - currently functions 
	#on keep or delete
	return render(request, 'upload.html', context)

def read_data(request, wb, lead, read_map):
	missing_fields = []

	wsIn = wb[read_map['wsIn']]
	if wsIn[read_map['start_loc']].value is None:
		return ["Empty file"]

	summary = [("Upload summary:")]
	wlrowNum = read_map['wlrowNumInit']
	if read_map['variable_colums_TF']:
		rows = wsIn[(read_map['in_section']).format(get_column_letter(wsIn.max_column), wsIn.max_row)]
	else: rows = wsIn[(read_map['in_section']).format(wsIn.max_row)]

	#The generic sheet has the option of reading 
	#in one experiment per sheet with all data
	if 'exp_name' in read_map:
		exp_name = wsIn[read_map['exp_name']].value
		if exp_name:
			#this is where we start reading and checking
			lead = wsIn[read_map['lead']].value
			if lead == None:
				missing_fields.append('lead')
			if 'IRB' in read_map:
				IRB = wsIn[read_map['IRB']].value
			if 'description' in read_map:
				des = wsIn[read_map['description']].value
			e_n = exp_exist_or_new(exp_name,lead,IRB = IRB, description = des)
		summary.append(e_n)
			

	#read samples and experiment from Input sheet
	#then read datasets from "Worklist" sheet
	#separating out QC
	for i in rows:
		# i in wsIn['B34:H63']: #.format(wsIn.max_row):
		#each record a dataset associated with a sample
		if i[read_map['sample_name']].value is None:
			break
			#All done with samples
		#wlrowNum +=1
		#wlRow = wb[read_map['wsWL']][wlrowNum]

		#Otherwise read it in
		if read_map['experiment_global']:
			e_n = exp_exist_or_new(wsIn[read_map['experiment_loc']].value, lead)
		else:
			e_n = exp_exist_or_new(i[int(read_map['experiment_loc'])].value, lead)
		experiment = Experiment.objects.all().get(_experimentName = e_n[2])
		summary.append(e_n)

		e_n = sample_exists_or_new(i[read_map['sample_name']].value, experiment, i, wsIn, read_map)
		sample = Sample.objects.all().get(_sampleName = e_n[2])
		summary.append(e_n)
		
	wsWL = wb[read_map['wsWL']]
	wlRows = wsWL[(read_map['wlRows']).format(wsWL.max_row)]
	inRows = wsIn[(read_map['in_section_lookup']).format(wsIn.max_row)]
	for wlRow in wlRows:
		if wlRow[read_map['dataset_name']].value is None:
			break #there isn't a dataset there
		#read in datasets
		sample_type = wlRow[read_map['wl_sample_type']].value
		if sample_type == 'QC':
			sample_name = str(lead+" lab QC")
			if Sample.objects.all().filter(_sampleName = sample_name).exists():
				sample = Sample.objects.all().get(_sampleName = sample_name)
				experiment = sample.experiment()
			else:
				if not 'QC_exp' in read_map:
					exp_name = (str(lead+" lab QC"))
				else: exp_name = str(wsWL[read_map['QC_exp']].value)
				#or wsIn if that's where QC information is defined'
				if Experiment.objects.all().filter(_experimentName = exp_name).exists():
					experiment = Experiment.objects.all().get(_experimentName =exp_name,  lead = lead)
					summary.append(["(DEFAULT)", 'QC Experiment: ', exp_name])
				else:
					experiment = Experiment( _experimentName = exp_name, _projectLead =  lead)
					experiment.save()
				sample = Sample( 
					_sampleName = sample_name,
					_storageCondition = "QC",
					_experiment = experiment,
					_storageLocation = "QC",
					_organism = "QC",
					)
				sample.save()
				summary.append(["(DEFAULT)", 'QC Sample: ', sample_name])
			sampleRow = []
		else: #Not a QC - it's a sample defined on input
			sampleNum = wlRow[read_map['wl_sample_num']].value
			sampleRow = findIn(sampleNum, inRows, read_map['lookup_column'])
			sample_name = sampleRow[read_map['lookup_sample']].value
			if Sample.objects.all().filter(_sampleName = sample_name).exists():
				sample = Sample.objects.all().get(_sampleName = sample_name)
			else: raise ValueError("No known sample")
			experiment = sample.experiment()
		#At this point both the sample and the experiment have been defined
		#"""
		
		e_n = dataset_exists_or_new(wlRow[read_map['dataset_name']].value, experiment, sample, sampleRow, wb, wsIn, wlRow, read_map)
		if sample_type == 'QC': e_n[1] = "QC Dataset: "
		summary.append(e_n)
		
	wlRow = None
	wsIn = None
	return summary

def findIn(val, rows, lookup_column):
	for line in rows:
		if line[lookup_column].value == val:
			return line
	return []

def upload_confirm(request, option = None):
	upload_status = request.session['upload_status']
	summary = request.session.get('upload_summary')
	upload_summary = []
	for i in summary:
		upload_summary.append(summary[i])
	print (upload_summary)
	upload_options = {'Confirm', 'Cancel'}
	context = {}
	
	if request.GET.get('option') == "Confirm":
		#print ("confirm")
		context['upload_status'] = 'Saved'
		context['summary'] = ''
		try: del request.session['upload_summary']
		except:
			request.session['message'] = 'Unable to verify save.'
			return redirect('success')
		request.session['upload_status'] = 'Saved.'
		return redirect('upload')
	elif request.GET.get('option') == 'Cancel':
		context['upload_status'] = 'Cancelling...'
		#print ("cancel")
		try:
			#get rid of read in data
			upload_summary = request.session.get('upload_summary')

			for i in upload_summary:
				if int(i) !=0: #
					v = upload_summary[i]
					if v[0] == NEW:
						#was new with this read in 
						#needs to be deleted
						if 'Experiment' in v[1]:
							#it's an experiment
							experiment = Experiment.objects.all().get(_experimentName = v[2])
							experiment.delete()
						elif 'Dataset' in v[1]:
							#may have been deleted with the experiment
							if Dataset.objects.all().filter(_datasetName = v[2]).exists():
								dataset = Dataset.objects.all().get(_datasetName = v[2])
								dataset.delete()
						elif 'Sample' in v[1]:
							#it's a sample -- it may have been deleted with the parent
							#experiment, so we check if it exists
							if Sample.objects.all().filter(_sampleName = v[2]).exists():
								s = Sample.objects.all().get(_sampleName = v[2])
								s.delete()
						else:
							print (v, "Delete Unsuccessful")
			request.session['upload_status'] = 'Upload Cancelled'
			del request.session['upload_summary']
		except: request.session['message'] = 'No upload found.'
		return redirect('upload')
	
	if len(upload_summary) >1: summary = upload_summary[1:]
	upload_status = upload_summary[0]
	context = {
		#'form':forms.UploadFileForm(),
		'upload_status':upload_status,
		'summary': summary,
		'upload_options': upload_options,
	}

	#Cancel options - currently functions 
	#on keep or delete
	return render(request, 'upload.html', context)
	
###NOT IMPLEMENTED YET 3-19-19###
def get_missing_fields(wb, read_map):
	missing_fields = []
	if 'missing_fields' in read_map:
		missing_fields = read_map['missing_fields']
	#the rest of our checking
	#Required Fields:
	#Exp. Name, Project Lead
	#	Design needs a name (exp does not need design)
	#
	#Individual ID, gender, age, health Status & extra_fields
	#
	#samples name, exp, storage_condition, location, organism
	#
	#dataset name, sample, instrument, file name, extension, path

	wsIn = wb[read_map['wsIn']]
	wsWL = wb[read_map['wsWL']]

	#bad logic
	if read_map['experiment_global']:
		name = wsIn[read_map['experiment_loc']].value
		if name == None:
			missing_fields.append('experiment_name')
		elif not experiments.filter(_experimentName = name).exists():
			#check for other experiment data
			if 'lead' in read_map:
				if wsIn[read_map['lead']].value == None:
					missing_fields.append('lead')
			elif not 'lead' in missing_fields: missing_fields.append('lead')
		elif 'lead' in missing_fields:
			missing_fields.remove('lead')
	else: 
		missing_fields.append('lead')
		missing_fields.append('IRB')
		missing_fields.append('description')

	if 'wsIndividual'in read_map:
		#check individuals
		if read_map['wsIndividual'] in wb:
			wsIndividual = wb[read_map['wsIndividual']]

	if read_map['variable_colums_TF']:
		rows = wsIn[(read_map['in_section']).format(get_column_letter(wsIn.max_column), wsIn.max_row)]
	else: rows = wsIn[(read_map['in_section']).format(wsIn.max_row)]

	#Do I now check each sample, the first one, or what?
	#Maybe the e_n functions report missing data 
	#and here we just catch overall missing categories of data?

	#Now I'm wondering if I need to ditch this and make it along with the read in?

	return missing_fields

def process_missing_fields(request):
	#if not 'missing_fields' in request.session:
	#	return redirect('upload')

	missing_fields = request.session['missing_fields']
	#"""
	#testing not verified
	form = forms.ListFieldsForm(extraFields = missing_fields)
	if request.method == 'POST':
		print ("POST")
		#Checked and sent to form but not yet recorded
		form = forms.ListFieldsForm(request.POST)
		request.session['missing_field_data'] = form.data
		print (form.data)

		upload_summary = request.session['upload_summary'] #to be used in template
		del request.session['missing_fields']
		del request.session['missing_field_data']
		return redirect ('upload_confirm')

	context = {'form':form, 'header':'Please address missing fields'}

	return render(request, 'title-form.html', context)	

#overload for additional information
def exp_exist_or_new(name, lead, IRB = None, description = None, ):
	experiments = Experiment.objects.all()
	if experiments.filter(_experimentName = name).exists():
		return [EXISTING, 'Experiment: ', name]
	#the experiment needs to be created
	newExp = Experiment(
		_experimentName = name,
		_projectLead =  lead,
	)
	if IRB: newExp.setIRB(IRB)
	if description: newExp.setComments()
	newExp.save()
	return [NEW, 'Experiment: ', name]# newExp.experimentID()]

def sample_exists_or_new(name, experiment, row, wsIn, read_map):
	samples = Sample.objects.all()
	if samples.filter(_sampleName = name).exists():
		return [EXISTING, 'Sample: ', name]

	comment = ""
	for c in read_map['comments_row']:
		comment += c
		comment += str(row[read_map['comments_row'][c]].value)+'\n'
	for c in read_map['comments_gen']:
		comment += c
		comment += str(wsIn[read_map['comments_gen'][c]].value)+'\n'

	if read_map['date_global']: date = wsIn[read_map['date_created']].value
	else: date = row[read_map['date_created']].value
	print (date)

	try:
		date = datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
	except:
		date = ''
	print (date)

	newSample = Sample(
		_sampleName = name,
		_storageCondition = "Processing",
		_experiment = experiment,
		_storageLocation = str(row[read_map['storage_location']].value),
		_organism = wsIn[(read_map['organism'])].value,
		_comments = comment,
	)
	if date !='': newSample.setDateCreated(date)
	newSample.save()
	return [NEW, 'Sample: ', name]

def dataset_exists_or_new(name, experiment, sample, row, wb, wsIn, wlRow, read_map):
	datasets = Dataset.objects.all()

	if datasets.filter(_datasetName = name).exists():
		return [EXISTING, 'Dataset: ', name]
	
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
		#If we wanted to try reverse-engineering the lookup function and get the rest of the setting information
		#it'd look a bit like this.
		#settings_column = wb[read_map['settings_sheet']][read_map['settings_keyword_column']]

		filename = wlRow[read_map['settings_file']].value
		try: ins.file = open(filename)
		except: 
			if ins.comments == None:
				ins.comments = filename
			else: 
				ins.comments = (str(ins.comments) + finename)
		ins.save()
		return [NEW, 'Instrument Setting: ', ins]

	summary = []
	ins_code = wsIn[read_map['inst_code']].value
	if ins_code == None: ins_code = ''
	else: ins_code = ' '+ins_code
	e_n = inst_exists_or_new(str(wsIn[read_map['instrument_type_loc']].value)+ins_code)
	print (e_n)
	initInstrument = e_n[2]
	if (e_n[0] == NEW): summary.append(e_n)
	if row != []:
		print (row)
		e_n = setting_exists_or_new(row[read_map['setting_loc']].value)
		setting = e_n[2]
	else: setting = None #wlRow[read_map['settings_file']]

	dataType = wsIn[read_map['data_type_loc']].value
	try: date = datetime.strptime(str(wsIn[read_map['date_loc']].value), '%m-%d-%Y').strftime('%Y-%m-%d')
	except: date = False

	wsWL = wb[read_map['wsWL']]
	if read_map['file_extension_from_excel']: extension = str(wlRow[read_map['file_extension']].value)
	else: extension = str(read_map['file_extension'])

	newDataset = Dataset(
		_datasetName = name,
		_experiment = experiment,
		_instrument = initInstrument,
		_fileName = str(wlRow[read_map['file_name']].value)+extension,
		_fileLocation = str(wlRow[read_map['file_location']].value),
		_instrumentSetting = setting,
		_type = dataType,
		#Commas after each value
		#acquisition dates
		#_status
		#_size
		#_fileHash
	)
	if date: newDataset.setDateCreated(date)
	newDataset.save()
	newDataset._sample.add(sample)

	return [NEW, 'Dataset: ', name]

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

def add_dataset(request):
    form =forms.AddDatasetForm()
    if request.method == 'POST':
        form =forms.AddDatasetForm(request.POST)
        if form.is_valid():
            new_Dataset = form.save()
            exp = new_Dataset.sample()[0].experiment()
            new_Dataset.setExperiment(exp)
            new_Dataset.save()
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
    desForm = forms.ExperimentalDesignForm()
    if request.method == 'POST':
        form =forms.AddExperimentForm(request.POST)
        desForm = forms.ExperimentalDesignForm(request.POST, request.FILES)
        if form.is_valid() and desForm.is_valid():
            new_Experiment = form.save(commit = False)
            newDes = desForm.save()
            new_Experiment.setExperimentalDesign(newDes)
            new_Experiment.save()
            return redirect('experiments')
    buttons = {
        #'New Experimental Design': 'add-experimental-design',
    }
    context = {
        'header':'Add Experiment',
        'form':form,
		'secFormHeading':'Experimental Design',
		'secForm':desForm,
        'buttons':buttons
    }

    return render(request, 'add-record.html', context)

def add_individual(request, experiment = None):
    if experiment == None:
        form = forms.SelectExperiment()# GetExperForm()
        context = {
            'form':form,
            'header':'Add Individual',
        }
        if request.method == 'POST':
            form = forms.SelectExperiment(request.POST)
            if form.is_valid():
                individual = form.save(commit = False)
                key = individual.experiment()._experimentID
            return redirect('add-individual', key)
        extra = []
        return render(request, 'title-form.html', context)
    else:
        try:
            experiment_set = Experiment.objects.all()
            exp = experiment_set.get(pk = experiment)
            extra = exp.experimentalDesign().extra_fields()
        except: extra = []
    
    form = forms.AddIndividualForm(extraFields = extra)
    if request.method == 'POST':
        form = forms.AddIndividualForm(request.POST, extraFields = extra)
        if form.is_valid():
            new_Individual = form.save(commit = False)
            #parses to JSON
            extraFieldData = {}
            for f in extra:
                extraFieldData[f] = form.data[f]
            new_Individual.setExtraFields(extraFieldData)
            new_Individual.setExperiment(exp)
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

    def get_exp(self, context):
        form = forms.SelectExperiment()
        if self.request.method == 'GET':
            form =forms.SelectExperiment(self.request.GET)
            if form.is_valid():
                i = form.save(commit = False)
                context['experiment'] = i.experiment()._experimentID
        context['filter_by_exp'] = form
        return context
	    
    def get_queryset(self, experiment = None):
        if experiment == None:
            queryset = Sample.objects.all()
        else:
            queryset = Sample.objects.filter(_experiment = experiment)
        return queryset

    #DataMan\Records\templates\Records\samples_list.html
    template_name = 'samples_list.html'
    context_object_name = 'sample'
    def get_context_data(self, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)
        context = self.get_exp(context, **kwargs)
        if 'experiment' in context:
            queryset = self.get_queryset(context['experiment'])
        else: queryset = self.get_queryset()
        table = SampleTable(queryset.order_by('-pk'))
        RequestConfig(self.request, paginate={'per_page': 25}).configure(table)
        context['table'] = table
        context['Title'] = 'Sample'
        return context

class DatasetView(ListView):
    model = Dataset

    def get_exp(self, context):
        form = forms.SelectExperiment()
        if self.request.method == 'GET':
            form =forms.SelectExperiment(self.request.GET)
            if form.is_valid():
                i = form.save(commit = False)
                context['experiment'] = i.experiment()._experimentID
        context['filter_by_exp'] = form
        return context
	    
    def get_queryset(self, experiment = None):
        if experiment == None:
            queryset = Dataset.objects.all()
        else:
            queryset = Dataset.objects.filter(_experiment = experiment)
        return queryset

    template_name = 'dataset_list.html'
    context_object_name = 'dataset'
    def get_context_data(self, **kwargs):
        context = super(DatasetView, self).get_context_data(**kwargs)
        context = self.get_exp(context, **kwargs)
        if 'experiment' in context:
            queryset = self.get_queryset(context['experiment'])
        else: queryset = self.get_queryset()
        table = DatasetTable(queryset.order_by('-pk'))
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

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        design = context['sample'].treatmentProtocol()
        if design != None:
            context['protocol'] = design
            context['protocol.description'] = design.description()
            if design.file():
                context['protocol_filename'] = basename(design.file().path)
                context['protocol_download'] =design.file().url
        return context

class DatasetDetailView(DetailView):
    instrumentSetting = "new"
    model = Dataset
    template = 'dataset_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        instrument = context['dataset'].instrument()
        context['instrument'] = instrument

        context['instrument.description'] = instrument.description()
        if instrument.file():
            context['instrument_filename'] = basename(instrument.file().path)
            context['instrument_download'] =instrument.file().url
        
        setting = context['dataset'].instrumentSetting()
        context['setting'] = setting
        
        if setting != None:
            context['setting.description'] = setting.description()
            if setting.file():
                context['setting_filename'] = basename(setting.file().path)
                context['setting_download'] =setting.file().url
        return context

class ExperimentDetailView(DetailView):
    model = Experiment
    template = 'experiment_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ExperimentDetailView, self).get_context_data(**kwargs)
        design = context['experiment'].experimentalDesign()
        context['design'] = design
        if design != None: 
            context['design.description'] = design.description()
            if design.file():
                context['design_filename'] = basename(design.file().path)
                context['design_download'] = design.file().url
        return context

class IndividualDetailView(DetailView):
	model = Individual
	template = 'individual_detail.html'