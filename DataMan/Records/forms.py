from django import forms
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from Records.models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class AddSampleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddSampleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sample
        fields = ['_sampleName',  '_experiment',
                  '_storageCondition', '_storageLocation', '_treatmentProtocol',
                  '_dateCreated','_organism', '_organismModifications']
        widgets = {'_dateCreated':DateInput()}
        
class AddDatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['_datasetName','_sample', '_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_acquisitionStart','_acquisitionEnd',
                  '_fileName','_fileLocation',
                  '_fileSize','_fileHash',]
        widgets = {
			'_dateCreated':DateInput(),
			'_acquisitionStart':DateInput(),#TimeInput(format='%m/%d/%Y %H:%M'),
			'_acquisitionEnd':DateInput(),
		}
    
    def validate(self):
	    #_experiment = _sample._experiment
        #any extra validation 
        return True

class AddExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['_experimentName','_projectLead','_teamMembers',
                  '_IRB','_experimentalDesign',]
