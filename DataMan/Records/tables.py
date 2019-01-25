import django_tables2 as tables
from django_tables2.utils import A
from Records.models import Dataset, Sample, Experiment


class DatasetTable(tables.Table):
    _datasetName = tables.LinkColumn('dataset-detail', args=[A('pk')])
    _sample = tables.LinkColumn('sample-detail', args=[A('_sample.pk')])
    #Experiment = tables.LinkColumn('experiment-detail', args=[A('_sample._experiment.pk')])

    class Meta:
        model = Dataset
        fields = ['_sample','_datasetName', '_instrumentSetting','_type',
                  '_operator','_status','_dateCreated','_fileLocation',
                  '_fileName',#'_acquisitionStart','_acquisitionEnd',
                  '_fileSize','_fileHash',]
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "None"

class SampleTable(tables.Table):
    _sampleName = tables.LinkColumn('sample-detail', args=[A('pk')])

    class Meta:
        model = Sample
        fields = ['_experiment','_sampleName',
                  '_storageCondition', '_storageLocation', '_treatmentProtocol',
                  '_dateCreated', '_organism', '_organismModifications']

class ExperimentTable(tables.Table):
    _experimentName = tables.LinkColumn('experiment-detail', args=[A('pk')])
    
    class Meta:
        model = Experiment
        fields = ['_experimentName','_projectLead',#'_teamMembers',
                  '_IRB','_experimentalDesign',]