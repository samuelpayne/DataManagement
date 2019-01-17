#These will be the url patterns for the records app
#Which keeps track of the records (Patient, Sample, Dataset, Experiments)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.records, name = 'records'),
    
    #add pages with form
    #probably seperate pages for each type ...?
    path('samples/add/', views.add_sample, name = 'add-sample'),
    path('archive/', views.archive, name = 'archive'),
         
    path('samples/', views.SampleView.as_view(), name = 'samples'),
    path('datasets/', views.DatasetView.as_view(), name = 'datasets'),
    path('experiments/', views.ExperimentView.as_view(), name = 'experiments'),
    #path('patients/', views.PatientView.as_view(), name = 'patients'),
    
    path('samples/<int:pk>/', views.SampleDetailView.as_view(), 
         name = 'samples-detail'),
]