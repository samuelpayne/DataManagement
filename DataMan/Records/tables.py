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
        fields = ['_experiment','_datasetName', '_instrument', '_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_fileLocation',
                  '_fileName',
                  '_fileSize', '_comments']

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