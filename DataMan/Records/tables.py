"""Project DataMan

These define the tables used in the archive view pages."""

import django_tables2 as tables
from django_tables2.utils import A
from Records.models import Dataset, Sample, Experiment, Individual


class DatasetTable(tables.Table):
    _datasetName = tables.LinkColumn('dataset-detail', args=[A('pk')])
    _experiment = tables.LinkColumn('experiment-detail', args=[A('_experiment.pk')])

    _dateCreated = tables.DateTimeColumn(format ='M d, Y')
    #_acquisitionStart = tables.DateTimeColumn(format ='M d, Y h:m')
    #_acquisitionEnd = tables.DateTimeColumn(format ='M d, Y h:m')

    class Meta:
        model = Dataset
        exclude = ['_datasetID','_sample','_acquisitionStart','_acquisitionEnd','_fileHash']

class SampleTable(tables.Table):
    _sampleName = tables.LinkColumn('sample-detail', args=[A('pk')])
    _experiment = tables.LinkColumn('experiment-detail', args=[A('_experiment.pk')])

    _dateCreated = tables.DateTimeColumn(format ='M d, Y')

    class Meta:
        model = Sample
        fields = ['_experiment','_sampleName',
                  '_storageCondition', '_storageLocation', '_treatmentProtocol',
                  '_dateCreated', '_organism', '_organismModifications', '_comments']

class ExperimentTable(tables.Table):
    _experimentName = tables.LinkColumn('experiment-detail', args=[A('pk')])
    _experimentalDesign = tables.TemplateColumn('{{record.experimentalDesign|slice:":25"}}...')
    _comments = tables.TemplateColumn('{{record.comments|slice:":25"}}...')
    
    class Meta:
        model = Experiment
        fields = ['_experimentName','_projectLead','_teamMembers',
                  '_IRB','_comments','_experimentalDesign',]

class IndividualTable(tables.Table):
    _individualIdentifier = tables.LinkColumn('individual-detail', args=[A('pk')])
    _experiment = tables.LinkColumn('experiment-detail', args=[A('_experiment.pk')])
    
    class Meta:
        model = Individual
        exclude = ['_individualID', '_extra_fields']