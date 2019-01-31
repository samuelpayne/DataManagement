import django_tables2 as tables
from django_tables2.utils import A
from Records.models import Dataset, Sample, Experiment


class DatasetTable(tables.Table):
    _datasetName = tables.LinkColumn('dataset-detail', args=[A('pk')])
    _sample = tables.LinkColumn('sample-detail', args=[A('_sample.pk')])
    _experiment = tables.LinkColumn('experiment-detail', args=[A('_experiment.pk')])

    _dateCreated = tables.DateTimeColumn(format ='M d, Y')

    class Meta:
        model = Dataset
        fields = ['_experiment', '_sample','_datasetName', '_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_fileLocation',
                  '_fileName','_acquisitionStart','_acquisitionEnd',
                  '_fileSize','_fileHash',]

class SampleTable(tables.Table):
    _sampleName = tables.LinkColumn('sample-detail', args=[A('pk')])
    _experiment = tables.LinkColumn('experiment-detail', args=[A('_experiment.pk')])
    dataset = tables.LinkColumn('dataset-detail', args=[A('dataset.pk')])
	
    _dateCreated = tables.DateTimeColumn(format ='M d, Y')

    class Meta:
        model = Sample
        fields = ['_experiment','_sampleName', 'dataset',
                  '_storageCondition', '_storageLocation', '_treatmentProtocol',
                  '_dateCreated', '_organism', '_organismModifications']

class ExperimentTable(tables.Table):
    _experimentName = tables.LinkColumn('experiment-detail', args=[A('pk')])
    
    class Meta:
        model = Experiment
        fields = ['_experimentName','_projectLead','_teamMembers',
                  '_IRB','_experimentalDesign',]