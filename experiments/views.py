from experiments.models import Dataset, DatasetItem
from experiments.serializers import DatasetSerializer, DatasetItemSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import filters


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
