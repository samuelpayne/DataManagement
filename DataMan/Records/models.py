from django.db import models
from datetime import datetime

#from django_mysql.models import ListCharField


class Dataset(models.Model):
    _datasetName = models.TextField(verbose_name='Dataset Name',
                                   unique=True)
    _datasetID = models.AutoField(verbose_name='Dataset ID', primary_key=True,
                                    unique=True)
    _sample = models.OneToOneField('Sample', on_delete=models.CASCADE,
                                  blank=False, null=False,verbose_name="Sample")
    _experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE,
                                   blank=True, null=True,verbose_name='Experiment')
    _instrument = models.ForeignKey('Instrument', verbose_name='Instrument', on_delete=models.SET_NULL, blank=False, null=True)
    _instrumentSetting = models.ForeignKey('InstrumentSetting',verbose_name="Instrument Setting", on_delete=models.SET_NULL, null=True, blank=True)
    _type = models.TextField(verbose_name='Type of data generated')
    _operator = models.TextField(verbose_name='Operator', help_text ="The team member who ran the machine.")
    _status = models.TextField(verbose_name='Status')
    _dateCreated = models.DateTimeField(verbose_name='Date Created', default=datetime.now)
    _fileLocation = models.TextField(verbose_name='Path to file location')
	####APPARENTLY THERE ARE FILEPATHFIELDS AND THAT MIGHT BE USEFULL####
    _fileName = models.TextField(verbose_name='File Name', null=True, blank=True)
    _acquisitionStart = models.DateTimeField(verbose_name='Acquisition Start',default=datetime.now)
    _acquisitionEnd = models.DateTimeField(verbose_name="Acquisition End", default=datetime.now)
    _fileSize = models.IntegerField(verbose_name='File Size', null=True, blank=True)
    _fileHash = models.TextField(verbose_name='File Hash', null=True, blank=True)


	#@property
	#def datasetName(self):
	#    return self.__datasetName
	#@datasetName.setter
	#def datasetName(self, datasetName)
	#    #checks
	#    self.__datasetName = datasetName
    def datasetName(self):
        return self._datasetName
    def datasetName(self, _val):
        if _val == 'fail-fail-fail': #whatever validation needs to happen
            #no change
            _datasetName
        _datasetName = _val
        return True
    def datasetID(self):
        return self._datasetID
    def sample(self):
        return self._sample
    def instrumentSetting(self):
        if self._instrumentSetting == 'fail-fail-fail':
            return "Failed"
        return self._instrumentSetting
    #def instrumentSetting(self, _val):
    #    self.instrumentSetting = _val
	
    def type(self):
        return self._type
    def operator(self):
        return self._operator
    def status(self):
        return self._status
    def dateCreated(self):
        return self._dateCreated
    def fileLocation(self):
        return self._fileLocation
    def fileName(self):
        return self._fileName
    def acquisitionStart(self):
        return self._acquisitionStart
    def acquisitionEnd(self):
        return self._acquisitionEnd
    def fileSize(self):
        return self._fileSize
    def fileHash(self):
        return self._fileHash

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
    _treatmentProtocol = models.TextField(verbose_name='Treatment Protocol', null=True, blank=True)
    _dateCreated = models.DateTimeField(verbose_name='Date Created', default=datetime.now)
    _organism = models.TextField(verbose_name='Organism')
    _organismModifications = models.TextField(verbose_name='Organism Modifications', default='None', null=True, blank=True)

    def sampleName(self):
        return self._sampleName
    def sampleID(self):
        return self._sampleID
    def experiment(self):
        return self._experiment
    def storageCondition(self):
        return self._storageCondition
    def storageLocation(self):
        return self._storageLocation
    def treatmentProtocol(self):
        return self._treatmentProtocol
    def dateCreated(self):
        return self._dateCreated
    def organism(self):
        return self._organism
    def organismModifications(self):
        return self._organismModifications

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

#class Protocol(models.Model):

#class Project(models.Model):

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

class Instrument(detailedField):
	def __str__(self):
		return self._name

class ExperimentDesign(detailedField):
	def __str__(self):
		return self._name