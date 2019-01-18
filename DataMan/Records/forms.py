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
        fields = ['datasetName','datasetID','sample','instrumentSetting','type',
                  'operator','status','dateCreated','fileLocation',
                  'fileName','acquisitionStart','acquisitionEnd',
                  'fileSize','fileHash',]

class AddExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['experimentName','experimentID','projectLead','teamMembers',
                  'IRB','experimentalDesign',]

