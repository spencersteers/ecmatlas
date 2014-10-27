from ecmdatabase.models import Tissue, Protein
from ecmdatabase.serializers import TissueSerializer, ProteinSerializer
from rest_framework import generics

class ProteinList(generics.ListCreateAPIView):
    resource_name = 'protein'
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer

class ProteinDetail(generics.RetrieveAPIView):
    resource_name = 'protein'
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer

class TissueList(generics.ListCreateAPIView):
    resource_name = 'tissue'
    queryset = Tissue.objects.all()
    serializer_class = TissueSerializer

class TissueDetail(generics.RetrieveAPIView):
    resource_name = 'tissue'
    queryset = Tissue.objects.all()
    serializer_class = TissueSerializer
