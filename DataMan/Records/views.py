from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from . import forms
import re
from Records.models import Sample, Dataset, Experiment
from django.forms.models import model_to_dict

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
        col_names = [re.sub(r'\w+\.\w+\.', '', str(i.verbose_name)) for i in model._meta.get_fields()]
        col_names = col_names[1:]  #using the [1:] so it skips the first item which just declares it is one to many or one to one
    else:
        results = []
        col_names = []
    data = {
    'type' : param,
    'show_table': param not in ['experiments','samples','datasets'],
    'query_results': results,
    'col_names': col_names,
    }
    """or:
    for type in RecordTypes:
        data[type] = type.objects.all().count()
        #or whatever you want this page to know"""
    return render(request, 'archive.html', context = data)

def create_new(request):
    return render(request, 'create-new.html',)

"""Page to add a sample"""
def add_sample(request):
    #check anything you want checked
    form =forms.AddSampleForm(request.POST)
    if form.is_valid():
        #do cool and important things with the information
        #form.check_date()
        new_Sample = form.save()
        return redirect('samples')

    context = {
        'form':form,
        'model':'Sample'
    }

    return render(request, 'add-record.html', context)

def add_dataset(request):
    form =forms.AddDatasetForm(request.POST)
    if form.is_valid():
        new_Dataset = form.save()
        return redirect('datasets')

    context = {
        'form':form,
        'model':'Dataset'
    }

    return render(request, 'add-record.html', context)

def add_experiment(request):
    form =forms.AddExperimentForm(request.POST)
    if form.is_valid():
        new_Experiment = form.save()
        return redirect('experiments')

    context = {
        'form':form,
        'model':'Experiment'
    }

    return render(request, 'add-record.html', context)
"""To edit a sample
    sample = Sample.objects.get(pk=pk) #get pk from url
    form =forms.AddSampleForm(request.POST, instance = sample)
    form.save()
    """

"""(type)Views will generate the list view pages
i.e., the list of samples"""
class SampleView(ListView):
    model = Sample
    queryset = Sample.objects.all()

    #DataMan\Records\templates\Records\samples_list.html
    template_name = 'samples_list.html'
    paginate_by = 25

class DatasetView(ListView):
    model = Dataset
    queryset = Dataset.objects.all()
    template_name = 'dataset_list.html'
    paginate_by = 25

class ExperimentView(ListView):
    model = Experiment
    queryset = Experiment.objects.all()
    template_name = 'experiment_list.html'
    paginate_by = 25

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
    model = Dataset
    template = 'dataset_detail.html'


class ExperimentDetailView(DetailView):
    model = Experiment
template = 'experiment_detail.html'
