from atlas.models import Tissue, Family, FunctionalGroup, Protein
from atlas.serializers import TissueSerializer, ProteinSerializer, FamilySerializer, FunctionalGroupSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import filters


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object


class ProteinList(generics.ListAPIView):

    resource_name = 'protein'
    serializer_class = ProteinSerializer

    def get_queryset(self):

        queryset = Protein.objects.all()
        gene_query = self.request.QUERY_PARAMS.get('gene_name', None)
        prot_query = self.request.QUERY_PARAMS.get('prot_acc', None)

        if gene_query is not None:
            queryset = queryset.filter(gene_name__startswith= gene_query)

        if prot_query is not None:
            queryset = queryset.filter(prot_acc__startswith= prot_query)

        return queryset


class ProteinDetail(generics.RetrieveAPIView):

    resource_name = 'protein'
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer


class TissueList(generics.ListAPIView):

    resource_name = 'tissue'
    queryset = Tissue.objects.all()
    serializer_class = TissueSerializer


class TissueDetail(generics.RetrieveAPIView):

    resource_name = 'tissue'
    queryset = Tissue.objects.all()
    serializer_class = TissueSerializer
    # lookup_field = 'slug'

# class TissueNameDetail(generics.RetrieveAPIView):
#     resource_name = 'tissue'
#     queryset = Tissue.objects.all()
#     serializer_class = TissueSerializer
#     lookup_field = 'name'


class FamilyList(generics.ListAPIView):

    resource_name = 'family'
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class FamilyDetail(generics.RetrieveAPIView):

    resource_name = 'family'
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class FunctionalGroupList(generics.ListAPIView):

    resource_name = 'functional_group'
    queryset = FunctionalGroup.objects.all()
    serializer_class = FunctionalGroupSerializer


class FunctionalGroupDetail(generics.RetrieveAPIView):

    resource_name = 'functional_group'
    queryset = FunctionalGroup.objects.all()
    serializer_class = FunctionalGroupSerializer