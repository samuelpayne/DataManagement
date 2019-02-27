import django_tables2 as tables
from django_tables2.utils import A
from Records.models import Dataset, Sample, Experiment, Individual


class DatasetTable(tables.Table):
    _datasetName = tables.LinkColumn('dataset-detail', args=[A('pk')])
    #_sample = tables.LinkColumn('sample-detail', args=[A('_sample.pk')])
    _experiment = tables.LinkColumn('experiment-detail', args=[A('_experiment.pk')])

    _dateCreated = tables.DateTimeColumn(format ='M d, Y')
    _acquisitionStart = tables.DateTimeColumn(format ='M d, Y h:m')
    _acquisitionEnd = tables.DateTimeColumn(format ='M d, Y h:m')

    class Meta:
        model = Dataset
        fields = ['_experiment','_datasetName', '_instrument', '_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_fileLocation',
                  '_fileName','_acquisitionStart','_acquisitionEnd',
                  '_fileSize','_fileHash', '_comments']

class SampleTable(tables.Table):
    _sampleName = tables.LinkColumn('sample-detail', args=[A('pk')])
    _experiment = tables.LinkColumn('experiment-detail', args=[A('_experiment.pk')])
    dataset = tables.LinkColumn('dataset-detail', args=[A('dataset.pk')], verbose_name = 'Dataset')
	
    _dateCreated = tables.DateTimeColumn(format ='M d, Y')

    class Meta:
        model = Sample
        fields = ['_experiment','_sampleName', 'dataset',
                  '_storageCondition', '_storageLocation', '_treatmentProtocol',
                  '_dateCreated', '_organism', '_organismModifications', '_comments']

class ExperimentTable(tables.Table):
    _experimentName = tables.LinkColumn('experiment-detail', args=[A('pk')])
    _experimentalDesign = tables.TemplateColumn('{{record.experimentalDesign|slice:":15"}}...')
    
    class Meta:
        model = Experiment
        fields = ['_experimentName','_projectLead','_teamMembers',
                  '_IRB','_experimentalDesign',]

class IndividualTable(tables.Table):
    _individualIdentifier = tables.LinkColumn('individual-detail', args=[A('pk')])
    _experiment = tables.LinkColumn('experiment-detail', args=[A('_experiment.pk')])
    
    class Meta:
        model = Individual
        exclude = ['_individualID', '_extra_fields']