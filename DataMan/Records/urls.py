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
         
    path('samples/', views.SampleView.as_view(),
         {'records_per_page' : 25}, name = 'samples'),
    path('datasets/', views.SampleView.as_view(),
         {'records_per_page' : 25}, name = 'datasets'),
    path('experiments/', views.SampleView.as_view(),
         {'records_per_page' : 25}, name = 'experiments'),
    path('patients/', views.SampleView.as_view(),
         {'records_per_page' : 25}, name = 'patients'),
    
    path('samples/<int:pk>/', views.SampleDetailView.as_view(), 
         name = 'samples-detail'),
]
