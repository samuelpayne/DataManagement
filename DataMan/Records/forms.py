from django import forms
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from Records.models import *

class AddSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['sampleName',  'experiment',
                  'storageCondition', 'storageLocation', 'treatmentProtocol',
                  'dateCreated', 'organism', 'organismModifications']

    """def check_date(self):
        date = self.cleaned_data['dateCreated']
        dt = timedelta(years=10)
        if (datetime.now()-dt) or date > (datetime.now()+timedelta(years=10)):
            raise forms.ValidationError("Invalid date")"""
        
class AddDatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['_datasetName','_sample', '_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_fileLocation',
                  '_fileName','_acquisitionStart','_acquisitionEnd',
                  '_fileSize','_fileHash',]

class AddExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['experimentName','projectLead','teamMembers',
                  'IRB','experimentalDesign',]
