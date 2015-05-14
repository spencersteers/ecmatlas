from experiments.models import Experiment, Dataset, DatasetItem, RelativeConcentration
from experiments.serializers import ExperimentSerializer, DatasetSerializer, DatasetItemSerializer, RelativeConcentrationSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import filters

class ExperimentList(generics.ListAPIView):

    resource_name = 'experiment'
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects.all()


class ExperimentDetail(generics.RetrieveAPIView):

    resource_name = 'experiment'
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects.all()


class DatasetList(generics.ListAPIView):

    resource_name = 'dataset'
    serializer_class = DatasetSerializer

    def get_queryset(self):
        queryset = Dataset.objects.filter(is_inserted=True)
        return queryset


class DatasetDetail(generics.RetrieveAPIView):

    resource_name = 'dataset'
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class DatasetItemList(generics.ListAPIView):

    resource_name = 'datasetitem'
    queryset = DatasetItem.objects.all()
    serializer_class = DatasetItemSerializer


class DatasetItemDetail(generics.RetrieveAPIView):

    resource_name = 'datasetitem'
    queryset = DatasetItem.objects.all()
    serializer_class = DatasetItemSerializer


class RelativeConcentrationList(generics.ListAPIView):

    resource_name = 'relativeconcentration'
    queryset = RelativeConcentration.objects.all()
    serializer_class = RelativeConcentrationSerializer


class RelativeConcentrationDetail(generics.RetrieveAPIView):

    resource_name = 'telativeconcentration'
    queryset = RelativeConcentration.objects.all()
    serializer_class = RelativeConcentrationSerializer
