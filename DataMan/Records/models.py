from django.db import models

class Dataset(models.Model):
    datasetName = models.TextField(verbose_name='Dataset Name',
                                   unique=True)
    datasetID = models.AutoField(verbose_name='Dataset ID', primary_key=True,
                                    unique=True)
    sample = models.OneToOneField('Sample', on_delete=models.CASCADE,
                                  blank=True, null=True)
    # instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    instrumentSetting = models.TextField(verbose_name='link to instrument settings')
    type = models.TextField(verbose_name='Type of data generated')
    operator = models.TextField(verbose_name='Operator')
    status = models.TextField(verbose_name='Status')
    dateCreated = models.DateTimeField(verbose_name='Date Created')
    fileLocation = models.TextField(verbose_name='Path to file location')
    fileName = models.TextField(verbose_name='File Name')
    acquisitionStart = models.TextField(verbose_name='Acquisition Start')
    acquisitionEnd = models.TextField(verbose_name="Acquisition End")
    fileSize = models.IntegerField(verbose_name='File Size')
    fileHash = models.TextField(verbose_name='File Hash')

    def getInstrumentSetting(self):
        if self.instrumentSetting == 'fail-fail-fail':
            return "Failed"
        return self.instrumentSetting

    def get_absolute_url(self):
        return reverse('dataset-detail', args=[str(self.datasetID)])

    def __str__(self):
        return self.datasetName


class Sample(models.Model):
    sampleName = models.TextField(verbose_name="Sample Name",
                                  unique=True)
    sampleID = models.AutoField(primary_key=True,
                                   unique=True)
    experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE,
                                   blank=True, null=True)
    # dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE,
    #                            blank = True, null = True)
    # preceedingSample = models.TextField(verbose_name='Preceeding Sample')
    storageCondition = models.TextField(verbose_name='Storage Condition')
    storageLocation = models.TextField(verbose_name='Storage Location')
    treatmentProtocol = models.TextField(verbose_name='Treatment Protocol')
    dateCreated = models.DateTimeField(verbose_name='Date Created')
    organism = models.TextField(verbose_name='Organism')
    organismModifications = models.TextField(verbose_name='Organism Modifications', default='None')

    # this sets the default sort
    class Meta:
        ordering = ['sampleName']

    def get_absolute_url(self):
        return reverse('sample-detail', args=[self.sampleID])

    def __str__(self):
        return self.sampleName


class Experiment(models.Model):
    experimentName = models.TextField(verbose_name='Experiment Name',
                                      unique=True)
    experimentID = models.AutoField(verbose_name='Experiment ID', primary_key=True,
                                       unique=True)
    projectLead = models.TextField(verbose_name='Project Lead')
    teamMembers = models.TextField(verbose_name='Team Members')
    IRB = models.IntegerField(verbose_name='IRB Number')
    # samples = models.ForeignKey(Sample, on_delete=models.CASCADE)
    # datasets = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    experimentalDesign = models.TextField(verbose_name='Experimental Design')

    def get_absolute_url(self):
        return reverse('experiment-detail', args=[str(self.experimentID)])

    def __str__(self):
        return self.experimentName
