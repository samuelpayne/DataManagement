from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from . import forms

from Records.models import Sample, Dataset, Experiment

# Create your views here.

"""Records named 'records'
    Give options:
     -view Archives
     -add records"""
def records(request):
    return render(request, 'records.html')

"""Archive home named 'archive'
    Allow type selection"""
def archive(request):
    #get general data
    data ={}
    #num_samples = samples.objects.all().count()
    #num_datasets = datasets.objects.all().count()
    """or:
    for type in RecordTypes:
        data[type] = type.objects.all().count()
        #or whatever you want this page to know"""
    return render(request, 'archive.html', context = data)

"""Page to add a sample"""
def add_sample(request):
    #check anything you want checked
    form =forms.AddSampleForm(request.POST)
    if form.is_valid():
        #do cool and important things with the information
        new_Sample = form.save()
        return redirect('samples')

    context = {
        'form':form,
        'model':'Sample'
    }
        
    return render(request, 'add-record.html', context)

def add_dataset(request):
    #check anything you want checked
    form =forms.AddDatasetForm(request.POST)
    if form.is_valid():
        #do cool and important things with the information
        new_Dataset = form.save()
        return redirect('datasets')

    context = {
        'form':form,
        'model':'Dataset'
    }
        
    return render(request, 'add-record.html', context)

def add_experiment(request):
    #check anything you want checked
    form =forms.AddExperimentForm(request.POST)
    if form.is_valid():
        #do cool and important things with the information
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

###   
#These classes would currently (1/15/19) cause
#issues since none of the models are defined
#yet
###
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

