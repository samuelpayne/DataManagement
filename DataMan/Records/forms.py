<<<<<<< HEAD
from django import forms
from django.core.exceptions import ValidationError
from Records.models import *

class AddSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['sampleName', 'sampleID', 'experiment',
                  'storageCondition', 'storageLocation', 'treatmentProtocol',
                  'dateCreated', 'organism', 'organismModifications']
=======
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
>>>>>>> 2fd595bee8dfe6b71d19d9c5a7f1981fd61e9b50
