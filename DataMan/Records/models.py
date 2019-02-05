from django.db import models
from datetime import datetime

#from django_mysql.models import ListCharField


class Dataset(models.Model):
    _datasetName = models.TextField(verbose_name='Dataset Name',
                                   unique=True)
    _datasetID = models.AutoField(verbose_name='Dataset ID', primary_key=True,
                                    unique=True)
    _sample = models.ManyToManyField('Sample', #on_delete=models.CASCADE,
                                  blank=False, null=False,verbose_name="Sample")
    _experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE,
                                   blank=True, null=True,verbose_name='Experiment')
    _instrument = models.ForeignKey('Instrument', verbose_name='Instrument', on_delete=models.SET_NULL, blank=False, null=True)
    _instrumentSetting = models.ForeignKey('InstrumentSetting',verbose_name="Instrument Setting",
                                    on_delete=models.SET_NULL, null=True, blank=True)
    if _instrument != 0:
        _instrument.limit_choices_to = {'_instrument': _instrument}
    _type = models.TextField(verbose_name='Type of data generated')
    _operator = models.TextField(verbose_name='Operator', help_text ="The team member who ran the machine.")
    #_status = models.ForeignKey("fileStatusOptions", on_delete=models.SET_NULL, verbose_name='Status', null=True)
    _status = models.TextField(verbose_name="File Status", null = True)
    _dateCreated = models.DateTimeField(verbose_name='Date Created', default=datetime.now)
    _fileLocation = models.TextField(verbose_name='Path to file location')
	####APPARENTLY THERE ARE FILEPATHFIELDS AND THAT MIGHT BE USEFULL####
    _fileName = models.TextField(verbose_name='File Name', null=True, blank=True)
    _acquisitionStart = models.DateTimeField(verbose_name='Acquisition Start',default=datetime.now)
    _acquisitionEnd = models.DateTimeField(verbose_name="Acquisition End", default=datetime.now)
    _fileSize = models.IntegerField(verbose_name='File Size', null=True, blank=True)
    _fileHash = models.TextField(verbose_name='File Hash', null=True, blank=True)
    _comments = models.TextField(verbose_name='Comments, Notes, or Details',blank=True,null=True)

    def datasetName(self):
        return self._datasetName
    def datasetName(self, value):
        self._datasetName = value
    def datasetID(self):
        return self._datasetID
    def datasetID(self, value):
        self._datasetID = value
    def sample(self):
        return self._sample
    def sample(self, value):
        self._sample = value
    def instrumentSetting(self):
        return self._instrumentSetting
    def instrumentSetting(self, _val):
        self.instrumentSetting = _val
    def type(self):
        return self._type
    def type(self, value):
        self._type = value
    def operator(self):
        return self._operator
    def operator(self, value):
        self._operator = value
    def status(self):
        return self._status
    def status(self, value):
        self._status = value
    def dateCreated(self):
        return self._dateCreated
    def dateCreated(self, value):
        self._dateCreated = value
    def fileLocation(self):
        return self._fileLocation
    def fileLocation(self, value):
        self._fileLocation = value
    def fileName(self):
        return self._fileName
    def fileName(self, value):
        self._fileName = value
    def acquisitionStart(self):
        return self._acquisitionStart
    def acquisitionStart(self, value):
        self._acquisitionStart = value
    def acquisitionEnd(self):
        return self._acquisitionEnd
    def acquisitionEnd(self, value):
        self._acquisitionEnd = value
    def fileSize(self):
        return self._fileSize
    def fileSize(self, value):
        self._fileSize = value
    def fileHash(self):
        return self._fileHash
    def fileHash(self, value):
        self._fileHash = value

    def get_absolute_url(self):
        return reverse('dataset-detail', args=[str(self._datasetID)])

    def __str__(self):
        return self._datasetName


class Sample(models.Model):
    _sampleName = models.TextField(verbose_name="Sample Name",
                                  unique=True)
    _sampleID = models.AutoField(primary_key=True,verbose_name="Sample ID",
                                   unique=True)
    _experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE,
                                   blank=True, null=True,verbose_name='Experiment')
    # preceedingSample = models.TextField(verbose_name='Preceeding Sample')
    _storageCondition = models.TextField(verbose_name='Storage Condition')
    _storageLocation = models.TextField(verbose_name='Storage Location')
    _treatmentProtocol = models.ForeignKey('Protocol', on_delete=models.SET_NULL, verbose_name='Treatment Protocol',null=True, blank=True)
    _dateCreated = models.DateTimeField(verbose_name='Date Created', default=datetime.now)
    _organism = models.TextField(verbose_name='Organism')
    _organismModifications = models.TextField(verbose_name='Organism Modifications', default='None', null=True, blank=True)
    _comments = models.TextField(verbose_name='Comments, Notes, or Details',blank=True,null=True)

    def sampleName(self):
        return self._sampleName
    def sampleName(self, value):
        self._sampleName = value
    def sampleID(self):
        return self._sampleID
    def sampleID(self, value):
        self._sampleID = value
    def experiment(self):
        return self._experiment
    def experiment(self, value):
        self._experiment = value
    def storageCondition(self):
        return self._storageCondition
    def storageCondition(self, value):
        self._storageCondition = value
    def storageLocation(self):
        return self._storageLocation
    def storageLocation(self, value):
        self._storageLocation = value
    def treatmentProtocol(self):
        return self._treatmentProtocol
    def treatmentProtocol(self, value):
        self._treatmentProtocol = value
    def dateCreated(self):
        return self._dateCreated
    def dateCreated(self, value):
        self._dateCreated = value
    def organism(self):
        return self._organism
    def organism(self, value):
        self._organism = value
    def organismModifications(self):
        return self._organismModifications
    def organismModifications(self, value):
        self._organismModifications = value

    # this sets the default sort
    class Meta:
        ordering = ['_sampleName']

    def get_absolute_url(self):
        return reverse('sample-detail', args=[self.sampleID])

    def __str__(self):
        return self._sampleName


class Experiment(models.Model):
    _experimentName = models.TextField(verbose_name='Experiment Name',
                                      unique=True)
    _experimentID = models.AutoField(verbose_name='Experiment ID', unique=True, primary_key=True)
    _projectLead = models.TextField(verbose_name='Project Lead')
    _teamMembers = models.TextField(verbose_name='Team Members',blank=True,null=True)
    _IRB = models.IntegerField(verbose_name='IRB Number',blank=True,null=True)
    _experimentalDesign = models.TextField(verbose_name='Experimental Design')
    _comments = models.TextField(verbose_name='Comments, Notes, or Details',blank=True,null=True)

    def experimentName(self):
        return self._experimentName
    def experimentName(self, value):
        self._experimentName = value
    def experimentID(self):
       return self._experimentID
    def experimentID(self, value):
        self._experimentID = value
    def projectLead(self):
        return self._projectLead
    def projectLead(self, value):
        self._projectLead = value
    def teamMembers(self):
        return self._teamMembers
    def teamMembers(self, value):
        self._teamMembers = value
    def IRB(self):
        return self._IRB
    def IRB(self, value):
        self._IRB = value
    def experimentalDesign(self):
        return self._experimentalDesign
    def experimentalDesign(self, value):
        self._experimentalDesign = value

    def get_absolute_url(self):
        return reverse('experiment-detail', args=[str(self._experimentID)])

    def __str__(self):
        return self._experimentName



class detailedField(models.Model):
	_name = models.CharField(unique=True, primary_key=True, 
			blank=False, null=False, max_length = 20)
	_description = models.TextField(verbose_name="Description",blank=True, null=True)
	_file = models.FileField(verbose_name='Related file or images',blank=True, null=True)

	def __str__(self):
		return self._name
	def name(self):
		return self._name
	def name(self, value):
		self._name = value
	def description(self):
		return self._description
	def description(self, value):
		self._description = value
	def file(self):
		return self._file
	def file(self, value):
		self._file = value
		
class InstrumentSetting(detailedField):
	_instrument = models.ForeignKey("Instrument", on_delete=models.CASCADE,
                                   blank=False, null=True,verbose_name='Instrument')
	def __str__(self):
		return self._name
	def instrument(self):
		return self._instrument
	def instrument(self, value):
		self._instrument = value

class Instrument(detailedField):
	def __str__(self):
		return self._name

class ExperimentalDesign(detailedField):
	def __str__(self):
		return self._name
		
class Protocol(detailedField):
	def __str__(self):
		return self._name

class fileStatusOption(models.Model):
	_option = models.CharField(unique=True, primary_key=True,
		blank=False, null=False, max_length = 20, verbose_name="Status")
	def __str__(self):
		return self._option