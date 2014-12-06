from ecmdatabase.models import Tissue, Family, FunctionalGroup, Protein, Dataset, DatasetItem
from ecmdatabase.serializers import TissueSerializer, ProteinSerializer
from ecmdatabase.forms import DatasetUploadForm

from django.core.context_processors import csrf


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse




class ProteinList(generics.ListAPIView):
    resource_name = 'protein'
    queryset = Protein.objects.all()
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


# class ExperimentList(generics.ListAPIView):
#     resource_name = 'experiment'
#     queryset = Experiment.objects.all()
#     serializer_class = ExperimentSerializer

# class ExperimentDetail(generics.RetrieveAPIView):
#     resource_name = 'experiment'
#     queryset = Experiment.objects.all()
#     serializer_class = ExperimentSerializer

# class ProteinHitList(generics.ListAPIView):
#     resource_name = 'protein_hit'
#     queryset = ProteinHit.objects.all()
#     serializer_class = ProteinHitSerializer

# class ProteinHitDetail(generics.RetrieveAPIView):
#     resource_name = 'protein_hit'
#     queryset = ProteinHit.objects.all()
#     serializer_class = ProteinHitSerializer


# class VariableModificationList(generics.ListAPIView):
#     resource_name = 'variable_modifications'
#     queryset = VariableModification.objects.all()
#     serializer_class = VariableModificationSerializer

# class VariableModificationDetail(generics.RetrieveAPIView):
#     resource_name = 'variable_modifications'
#     queryset = VariableModification.objects.all()
#     serializer_class = VariableModificationSerializer

#

from ecmdatabase.dataset_parser import parse_to_items
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

    dataset.is_inserted = True
    dataset.save()


def dataset_upload(request):
    if request.POST:
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = DatasetUploadForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['datasets'] = Dataset.objects.all()

    return render_to_response('upload.html', args)