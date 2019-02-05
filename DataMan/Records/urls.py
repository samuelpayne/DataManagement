#These will be the url patterns for the records app
#Which keeps track of the records (Patient, Sample, Dataset, Experiments)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.records, name = 'records'),

    #add pages with form
    #probably seperate pages for each type ...?
	path('about/', views.about, name='about'),
    path('add/', views.create_new, name = 'create-new'),
    path('add/samples/', views.add_sample, name = 'add-sample'),
    path('add/datasets/', views.add_dataset, name = 'add-dataset'),
    path('add/experiments/', views.add_experiment, name = 'add-experiment'),

	
    #path('add/samples/bulk', views.add_sample_bulk, name = 'add-samples-bulk'),

	#for editing 
    path('add/experiments/<int:pk>/', views.edit_experiment, name = 'edit-experiment'),
    path('add/samples/<int:pk>/', views.edit_sample, name = 'edit-sample'),
    path('add/datasets/<int:pk>/', views.edit_dataset, name = 'edit-dataset'),

    path('add/instrument/', views.add_instrument, name = 'add-instrument'),

    path('archive/', views.archive, name = 'archive'),
    #url(regex=r'type=(.*)$', view='views.archive'),
    path('samples/', views.SampleView.as_view(), name = 'samples'),
    path('datasets/', views.DatasetView.as_view(), name = 'datasets'),
    path('experiments/', views.ExperimentView.as_view(), name = 'experiments'),
    #path('patients/', views.PatientView.as_view(), name = 'patients'),

    path('samples/<int:pk>/', views.SampleDetailView.as_view(),
         name = 'sample-detail'),
    path('datasets/<int:pk>/', views.DatasetDetailView.as_view(),
         name = 'dataset-detail'),
    path('experiments/<int:pk>/', views.ExperimentDetailView.as_view(),
         name = 'experiment-detail'),
]
