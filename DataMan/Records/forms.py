from django import forms
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from Records.models import *

STATUS_OPTIONS = [#Probably eventually replace with something not hard coded in
    ('In Progress','In Progress'), #Maybe a fixture, maybe just add them manually 
    ('Submitted','Submitted'),     # once it's uploaded
    ('Analyzed','Analyzed'),
    ('Released','Released'),
    ('Archived','Archived'),
    ('Deleted','Deleted'),
    ('Revoked','Revoked'),
    ('Replaced','Replaced')
    ]

class detailedFieldWidget(forms.MultiWidget):
	def __init__(self, attrs = None):
		widgets={
			'_name': forms.CharField(max_length = 20),
			'_description': forms.Textarea(),#verbose_name="Description"),
			'_file': forms.FileField()#verbose_name='Related file or images')
		}
		super(detailedFieldWidget, self).__init__(widgets, attrs)

	def decompress(self, value):
		if value:
			return[value.name(), value.description(), value.file()]
		return[None,None,None]

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
	input_type = 'time' #make it look nice here

class DateTimeInput(forms.MultiWidget):
	def __init__(self, attrs = None,date_format=None, time_format=None):
		widgets=(DateInput(attrs=attrs),
			forms.TimeInput(attrs=attrs, format=time_format))
		super(DateTimeInput, self).__init__(widgets, attrs)

	def decompress(self, value):
		if value:
			return [value.date(), value.time().replace(microsecond=0)]
		return [None, None]

class AddSampleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddSampleForm, self).__init__(*args, **kwargs)
		
    def __name__(self, *args, **kwargs):
        super(AddSampleForm, self).__name__

    class Meta:
        model = Sample
        fields = ['_sampleName',  '_experiment',
                  '_storageCondition', '_storageLocation', '_treatmentProtocol',
                  '_dateCreated','_organism', '_organismModifications', '_comments']
        widgets = {'_dateCreated':DateInput()}
        
class AddDatasetForm(forms.ModelForm):
    _status = forms.CharField(label='File Status', widget=forms.Select(choices=STATUS_OPTIONS))
    class Meta:
        model = Dataset
        fields = ['_datasetName','_sample', '_instrument','_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_acquisitionStart','_acquisitionEnd',
                  '_fileName','_fileLocation',
                  '_fileSize','_fileHash', '_comments']
        widgets = {
			#'_instrument':detailedFieldWidget(),
			'_dateCreated':DateInput(),
			'_acquisitionStart':DateTimeInput(),#TimeInput(format='%m/%d/%Y %H:%M'),
			'_acquisitionEnd':DateTimeInput(),
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