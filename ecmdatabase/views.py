from ecmdatabase.models import Tissue, Protein, Experiment, ProteinHit, VariableModification
from ecmdatabase.serializers import TissueSerializer, ProteinSerializer, ExperimentSerializer, ProteinHitSerializer, VariableModificationSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import filters
import django_filters
from urllib.parse import urlparse, urlencode


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse



class ProteinFilter(django_filters.FilterSet):
    #new_gene_name = django_filters.CharFilter(name="gene_name")
    new_gene_name = django_filters.CharFilter(name="gene_name",lookup_type="contains")
    class Meta:
        model = Protein
        #fields = ['gene_name']
        fields = ['new_gene_name']

class ProteinList(generics.ListCreateAPIView):
    resource_name = 'protein'

    def get_queryset(self):
        
        queryset = Protein.objects.all()

        gene_query = self.request.QUERY_PARAMS.get('gene_name', None)
        prot_query = self.request.QUERY_PARAMS.get('prot_acc', None)



        if gene_query is not None:
          queryset = queryset.filter(gene_name__startswith= gene_query)


        if prot_query is not None:
            queryset = queryset.filter(prot_acc__startswith= prot_query) 

        return queryset

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


class ExperimentList(generics.ListCreateAPIView):
    resource_name = 'experiment'
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

class ExperimentDetail(generics.RetrieveAPIView):
    resource_name = 'experiment'
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class ProteinHitList(generics.ListCreateAPIView):
    resource_name = 'protein_hit'
    queryset = ProteinHit.objects.all()
    serializer_class = ProteinHitSerializer


class ProteinHitDetail(generics.RetrieveAPIView):
    resource_name = 'protein_hit'
    queryset = ProteinHit.objects.all()
    serializer_class = ProteinHitSerializer


class VariableModificationList(generics.ListCreateAPIView):
    resource_name = 'variable_modifications'
    queryset = VariableModification.objects.all()
    serializer_class = VariableModificationSerializer

class VariableModificationDetail(generics.RetrieveAPIView):
    resource_name = 'variable_modifications'
    queryset = VariableModification.objects.all()
    serializer_class = VariableModificationSerializer

