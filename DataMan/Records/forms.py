from django import forms
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from Records.models import *

STATUS_OPTIONS = [#Probably eventually replace with something not hard coded in
    ('In Progress','In Progress'),
    ('Submitted','Submitted'),
    ('Analyzed','Analyzed'),
    ('Released','Released'),
    ('Archived','Archived'),
    ('Deleted','Deleted'),
    ('Revoked','Revoked'),
    ('Replaced','Replaced')
    ]

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'
	#so I think the aquisitions will want time, too,
	#but haven't gotten it to work yet

class AddSampleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddSampleForm, self).__init__(*args, **kwargs)
		
    def __name__(self, *args, **kwargs):
        super(AddSampleForm, self).__name__

    class Meta:
        model = Sample
        fields = ['_sampleName',  '_experiment',
                  '_storageCondition', '_storageLocation', '_treatmentProtocol',
                  '_dateCreated','_organism', '_organismModifications']
        widgets = {'_dateCreated':DateInput()}
        
class AddDatasetForm(forms.ModelForm):
    _status = forms.CharField(label='File Status', widget=forms.Select(choices=STATUS_OPTIONS))
    class Meta:
        model = Dataset
        fields = ['_datasetName','_sample', '_instrument','_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_acquisitionStart','_acquisitionEnd',
                  '_fileName','_fileLocation',
                  '_fileSize','_fileHash',]
        widgets = {
			'_dateCreated':DateInput(),
			'_acquisitionStart':DateInput(),#TimeInput(format='%m/%d/%Y %H:%M'),
			'_acquisitionEnd':DateInput(),
			#'_status':forms.Select(choices=STATUS_OPTIONS)
		}

class AddExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['_experimentName','_projectLead','_teamMembers',
                  '_IRB','_experimentalDesign', '_comments',]

class AddInstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        exclude = []

class AddInstrumentSettingForm(forms.ModelForm):
    class Meta:
        model = InstrumentSetting
        exclude = []