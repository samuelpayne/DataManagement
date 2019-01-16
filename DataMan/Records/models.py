from django.db.import models

class Dataset (models.Model):
    datasetName = models.TextField(help_text='Dataset Name')
    datasetID = models.IntegerField(help_text='Dataset ID')
    # sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    # instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    instrumentSetting = models.TextField(help_text='link to instrument settings')
    type = models.TextField(help_text='Type of data generated')
    operator = models.TextField(help_text='Operator')
    status = models.TextField(help_text='Status')
    dateCreated = models.DateTimeField()
    fileLocation = models.TextField(help_text='Path to file location')
    fileName = models.TextField(help_text='File Name')
    acquisitionStart = models.TextField(help_text='Acquisition Start')
    acquisitionEnd = models.TextField(help_text="Acquisition End")
    fileSize = models.IntegerField(help_text='File Size')
    fileHash = models.TextField(help_text='File Hash')

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.my_field_name

class Sample (models.Model):
    sampleName = models.TextField(help_text='Sample Name')
    sampleID = models.IntegerField(help_text='Integer Field')
    # experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE)
    datasets = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    # preceedingSample = models.TextField(help_text='Preceeding Sample')
    storageCondition = models.TextField(help_text='Storage Condition')
    storageLocation = models.TextField(help_text='Path to storage location')
    treatmentProtocol = models.TextField(help_text='Treatment Protocol')
    dateCreated = models.DateTimeField()
    organism = models.TextField(help_text='Organism')
    organismModifications = models.TextField(help_text='Organism Modifications')

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.my_field_name

class Experiment(models.Model):
    experimentName = models.TextField(help_text='Experiment Name')
    experimentID = models.IntegerField(help_text='Experiment ID')
    projectLead = models.TextField(help_text='Project Lead')
    teamMembers = models.TextField(help_text='Team Members')
    IRB = models.IntegerField(help_text='IRB Number')
    samples = models.ForeignKey(Sample, on_delete=models.CASCADE)
    datasets = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    experimentalDesign = models.TextField(help_text='Experimental Design')

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.my_field_name
