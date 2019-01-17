from django import forms
from django.core.exceptions import ValidationError
from Records.models import *

class AddSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['sampleName', 'sampleID', 'experiment',
                  'storageCondition', 'storageLocation', 'treatmentProtocol',
                  'dateCreated', 'organism', 'organismModifications']
        
class AddDatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['datasetName','datasetID','sample']
        #add the rest before it will work--none are null-enabled
