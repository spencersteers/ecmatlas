from ecmdatabase.models import Protein
from ecmdatabase.serializers import ProteinSerializer
from rest_framework import generics


class ProteinList(generics.ListCreateAPIView):
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer

class ProteinDetail(generics.RetrieveAPIView):
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer
