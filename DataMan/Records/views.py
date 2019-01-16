from django.shortcuts import render

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

###   
#These classes would currently (1/15/19) cause
#issues since none of the models are defined
#yet
###
"""(type)Views will generate the list view pages
i.e., the list of samples""
class samplesView(ListView):
    model = sample
    queryset = tree.objects.all()

    #DataMan\Records\templates\Records\samples_list.html
    template_name = 'samples_list.html'
    paginate_by = records_per_page

""named (type)-detail, these are the detail view
pages generated for the specific record
Ex: sample 1234, dataset 3""
class samplesDetailView(DetailView):
    model = sample
    template = 'samples.html'
    #"""


