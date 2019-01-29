from django import forms
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from Records.models import *

class AddSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['_sampleName',  '_experiment',
                  '_storageCondition', '_storageLocation', '_treatmentProtocol',
                  '_dateCreated', '_organism', '_organismModifications']
        
class AddDatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['_datasetName','_sample', '_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_fileLocation',
                  '_fileName','_acquisitionStart','_acquisitionEnd',
                  '_fileSize','_fileHash',]
    
    def validate(self):
	    #_experiment = _sample._experiment
        #any extra validation 
        return True

class AddExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['_experimentName','_projectLead','_teamMembers',
                  '_IRB','_experimentalDesign',]
