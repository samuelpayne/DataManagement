#These will be the url patterns for the records app
#Which keeps track of the records (Patient, Sample, Dataset, Experiments)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.records, name = 'records'),
    
    #add pages with form 
    #path('add/<type>', views.addView.as_view(), name = 'add'),
    path('archive/', views.archive, name = 'archive'),
         
    #path('samples/', views.sampleView.as_view(),
    #     {'records_per_page' : 25}, name = 'samples'),
    #path('samples/<int:pk>/', views.sampleDetailView.as_view(), 
    #     name = 'samples-detail'),
]
