"""Project DataMan

These use the django forms to make
    data entry easy."""

from django import forms
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from Records.models import *
import json

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

class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        exclude = []
class InstrumentSettingForm(forms.ModelForm):
    class Meta:
        model = InstrumentSetting
        exclude = []
class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        exclude = []
class fileStatusOptionForm(forms.ModelForm):
    class Meta:
        model = fileStatusOption
        exclude = []
class ExperimentalDesignForm(forms.ModelForm):
    class Meta:
        model = ExperimentalDesign
        exclude = []


class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'
    #make it look nice here
class DateTimeInput(forms.MultiWidget):
    def __init__(self, attrs = None,date_format=None, time_format='%H:%M'):
        widgets=(DateInput(attrs=attrs),
            forms.TimeInput(attrs=attrs, format=time_format))
        super(DateTimeInput, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(second = 0, microsecond=0)]
        return [None, None]


class UploadFileForm(forms.ModelForm):
    readFail = False
    class Meta:
        model = FileRead
        fields = ['_File', 'lead']

    def __init__(self,  *args, extraFields=None, **kwargs,):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        if extraFields!=None:
            for f in extraFields:
                self.fields[f] = forms.CharField(label=f)

    def clean(self):
        data = self.cleaned_data
        if self.readFail: #conditionals from views
            raise forms.ValidationError('Invalid file')
        else:
            return data

class ListFieldsForm(forms.ModelForm):
    class Meta:
        model = FileRead
        fields = []
    def __init__(self,  *args, extraFields=None, **kwargs):
        super(ListFieldsForm, self).__init__(*args, **kwargs)
        if extraFields!=None:
            for f in extraFields:
                self.fields[f] = forms.CharField(label=f)
    def save(self):
        return self.cleaned_data

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

class SelectExperiment(forms.ModelForm):
    _experiment = forms.ModelChoiceField(label='Experiment', queryset=Experiment.objects.all(), widget=forms.Select(attrs={"onChange":'form.submit()'}))
    class Meta:
        model = Individual
        fields = ['_experiment']

class AddIndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        exclude = ['_individualID','_extra_fields', '_experiment']
    def __init__(self,  *args,extraFields=None, **kwargs,):
        super(AddIndividualForm, self).__init__(*args, **kwargs)
        if extraFields!=None:
            for f in extraFields:
                self.fields[f] = forms.CharField(label=f)

class AddDatasetForm(forms.ModelForm):
    _status = forms.CharField(label='File Status', widget=forms.Select(choices=STATUS_OPTIONS))
    class Meta:
        model = Dataset
        fields = ['_datasetName','_sample', '_instrument','_instrumentSetting','_type',
                  '_operator','_dateCreated','_acquisitionStart','_acquisitionEnd',
                  '_status','_fileName','_fileLocation',
                  '_fileSize', '_comments']
        widgets = {
            '_dateCreated':DateInput(),
            '_acquisitionStart':DateTimeInput(),
            '_acquisitionEnd':DateTimeInput(),
        }

class AddExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['_experimentName','_projectLead','_teamMembers',
                  '_IRB', '_comments',]

class BackUpSelectForm(forms.ModelForm):
    #if backups are force-daily, calender widget makes sense
    #otherwise we want a dropdown of available backups
    date = forms.CharField(label='Restore from', widget=DateInput)
    class Meta:
        model = BackupFile
        fields = ['date']
    
    def clean(self):
        data = self.cleaned_data
        if BackupFile.objects.all().filter(date = data['date']).exists() == False:
            raise forms.ValidationError('No backup available for that date.')
        else:
            return data