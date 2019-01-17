from django import forms
from django.core.exceptions import ValidationError
from Records.models import *

class AddSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['sampleName', 'sampleID', 'experiment',
                  'storageCondition', 'storageLocation', 'treatmentProtocol',
                  'dateCreated', 'organism', 'organismModifications']
