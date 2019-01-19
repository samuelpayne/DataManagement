from django import forms
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from Records.models import *

class AddSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['sampleName', 'sampleID', 'experiment',
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
        fields = ['datasetName','datasetID','sample','instrumentSetting','type',
                  'operator','status','dateCreated','fileLocation',
                  'fileName','acquisitionStart','acquisitionEnd',
                  'fileSize','fileHash',]

class AddExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['experimentName','experimentID','projectLead','teamMembers',
                  'IRB','experimentalDesign',]