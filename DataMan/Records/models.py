from django.db import models

class Dataset(models.Model):
    _datasetName = models.TextField(verbose_name='Dataset Name',
                                   unique=True)
    _datasetID = models.AutoField(verbose_name='Dataset ID', primary_key=True,
                                    unique=True)
    _sample = models.OneToOneField('Sample', on_delete=models.CASCADE,
                                  blank=False, null=False,verbose_name="Sample")
    # instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    _instrumentSetting = models.TextField(verbose_name='link to instrument settings')
    _type = models.TextField(verbose_name='Type of data generated')
    _operator = models.TextField(verbose_name='Operator')
    _status = models.TextField(verbose_name='Status')
    _dateCreated = models.DateTimeField(verbose_name='Date Created')
    _fileLocation = models.TextField(verbose_name='Path to file location')
    _fileName = models.TextField(verbose_name='File Name')
    _acquisitionStart = models.TextField(verbose_name='Acquisition Start')
    _acquisitionEnd = models.TextField(verbose_name="Acquisition End")
    _fileSize = models.IntegerField(verbose_name='File Size')
    _fileHash = models.TextField(verbose_name='File Hash')


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
            return False
        _datasetName = _val
        return True
    def datasetID(self):
        return self._datasetID
    def sample(self):
        return self._sample
    def instrumentSetting(self):
        if self._instrumentSetting != 'fail-fail-fail':
            return "Not Failed"
        return self._instrumentSetting
    def instrumentSetting(self, _val):
        self.instrumentSetting = _val
	
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
    _treatmentProtocol = models.TextField(verbose_name='Treatment Protocol')
    _dateCreated = models.DateTimeField(verbose_name='Date Created')
    _organism = models.TextField(verbose_name='Organism')
    _organismModifications = models.TextField(verbose_name='Organism Modifications', default='None')

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
    _teamMembers = models.TextField(verbose_name='Team Members')
    _IRB = models.IntegerField(verbose_name='IRB Number')
    _experimentalDesign = models.TextField(verbose_name='Experimental Design')

    def experimentName(self):
        return self._experimentName
    def experimentID(self):
       return self._experimentID
    def projectLead(self):
        return self._projectLead
    def teamMembers(self):
        return self._teamMembers
    def IRB(self):
        return self._IRB
    def experimentalDesign(self):
        return self._experimentalDesign

    def get_absolute_url(self):
        return reverse('experiment-detail', args=[str(self._experimentID)])

    def __str__(self):
        return self._experimentName
