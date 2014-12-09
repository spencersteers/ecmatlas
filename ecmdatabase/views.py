from ecmdatabase.models import Tissue, Family, FunctionalGroup, Protein, Dataset, DatasetItem
from ecmdatabase.serializers import TissueSerializer, ProteinSerializer, FamilySerializer, FunctionalGroupSerializer, DatasetSerializer, DatasetItemSerializer
from ecmdatabase.forms import DatasetUploadForm

from django.core.context_processors import csrf


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import filters
# import django_filters
from urllib.parse import urlparse, urlencode


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# class ProteinFilter(django_filters.FilterSet):
#     #new_gene_name = django_filters.CharFilter(name="gene_name")
#     new_gene_name = django_filters.CharFilter(name="gene_name",lookup_type="contains")
#     class Meta:
#         model = Protein
#         #fields = ['gene_name']
#         fields = ['new_gene_name']

class ProteinList(generics.ListAPIView):
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


class TissueList(generics.ListAPIView):
    resource_name = 'tissue'
    queryset = Tissue.objects.all()
    serializer_class = TissueSerializer

class TissueDetail(generics.RetrieveAPIView):
    resource_name = 'tissue'
    queryset = Tissue.objects.all()
    serializer_class = TissueSerializer


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



class DatasetList(generics.ListAPIView):
    resource_name = 'dataset'
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

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


# File uploads
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.files.uploadedfile import UploadedFile
from ecmdatabase.dataset_parser import parse_to_items
import json
import datetime

@csrf_exempt
def dataset_delete(request, dataset_id):
    if request.method == 'GET' or request.method == 'POST':
        dataset = get_object_or_404(Dataset, pk=dataset_id)
        dataset.delete()
        return HttpResponse(str(dataset_id))
    else:
        return HttpResponseBadRequest('Only POST accepted')



@csrf_exempt
def dataset_insert(request, dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)

    file_name = dataset.data_file.path

    dataset_items = parse_to_items(file_name)

    for item in dataset_items:

        family, is_new_family = Family.objects.get_or_create(name=item['family_name'])
        functional_group, is_new_fg = FunctionalGroup.objects.get_or_create(name=item['functional_group_name'])


        protein, is_new_protein = Protein.objects.get_or_create(
                                        sequence=item['sequence'],
                                        gene_name=item['gene_name'],
                                        protein_name=item['protein_name'],
                                        species=item['species_name'],
                                        family=family,
                                        functional_group=functional_group
                                    )

        tissue, is_new_tissue = Tissue.objects.get_or_create(name=item['tissue_name'])
        protein.tissues.add(tissue)
        protein.save()

        dataset_item = DatasetItem(
                                protein=protein,
                                tissue=tissue,
                                functional_group=functional_group,
                                family=family,
                                species=item['species_name'],
                                dataset=dataset,
                                peptide_sequence=item['sequence'],
                                gene=item['gene_name'],
                                molecular_weight=item['molecular_weight'],
                                tissue_weight_norm=item['tissue_weight_norm']
                            )
        dataset_item.save()

    dataset.inserted_at = datetime.datetime.now()
    dataset.is_inserted = True
    dataset.save()

    return HttpResponse(str(dataset.id))

@csrf_exempt
def dataset_upload(request):
    if request.method == 'POST':
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        #writing file manually into model
        #because we don't need form of any type.
        dataset = Dataset()
        dataset.name=str(filename)
        dataset.data_file=file
        dataset.save()

        #getting url for photo deletion
        file_delete_url = '/datasets/delete/'
        file_insert_url = '/datasets/insert/'

        #getting file url here
        file_url = dataset.data_file.url

        #getting thumbnail url using sorl-thumbnail

        #generating json response array
        result = {"files": []}
        result["files"].append({"name":filename,
                               "size":file_size,
                               "url":file_url,
                               "deleteUrl":file_delete_url+str(dataset.pk)+'/',
                               "deleteType":"POST",
                               "insertUrl":file_insert_url+str(dataset.pk)+'/',
                            })
        response_data = json.dumps(result)
        return HttpResponse(response_data, content_type='application/json')


    else:
        return render_to_response('upload.html')

@csrf_exempt
def dataset_uploadfiles(request):
    datasets = Dataset.objects.filter(is_inserted=True)
    result = {"files": []}
    for dataset in datasets:

        file_delete_url = '/datasets/delete/'
        file_insert_url = '/datasets/insert/'

        item = {
            "name": dataset.name,
            "url": dataset.data_file.url,
            "deleteUrl": file_delete_url+str(dataset.pk)+'/',
            "deleteType":"POST",
        }
        if not dataset.is_inserted:
            item["insertUrl"] = file_insert_url+str(dataset.pk)+'/'


        result["files"].append(item)

    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')
