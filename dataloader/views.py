from urllib.parse import urlparse, urlencode
import json
import datetime

from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from experiments.models import Dataset, DatasetItem
from atlas.models import Tissue, Family, FunctionalGroup, Protein
from dataloader.forms import DatasetUploadForm
from dataloader.tasks import parse_dataset

from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required()
def dataset_delete(request, dataset_id):
    if request.method == 'GET' or request.method == 'POST':
        dataset = get_object_or_404(Dataset, pk=dataset_id)
        dataset.delete()

        return HttpResponse(str(dataset_id))
    else:
        return HttpResponseBadRequest('Only POST accepted')


@csrf_exempt
@login_required()
def dataset_insert(request, dataset_id):
    parse_dataset.delay(dataset_id)

    return HttpResponse(str(dataset_id))

    # '''
    # After dataset is uploaded and inserted into the database
    # the items are parsed from the csv and items are inserted into
    # the database.
    # '''
    # dataset = Dataset.objects.get(pk=dataset_id)
    # file_name = dataset.data_file.path
    # dataset_items = parse_to_items(file_name)

    # for item in dataset_items:

    #     family, is_new_family = Family.objects.get_or_create(name=item['family_name'])
    #     functional_group, is_new_fg = FunctionalGroup.objects.get_or_create(name=item['functional_group_name'])

    #     protein, is_new_protein = Protein.objects.get_or_create(
    #                                     sequence=item['sequence'],
    #                                     gene_name=item['gene_name'],
    #                                     protein_name=item['protein_name'],
    #                                     species=item['species_name'],
    #                                     family=family,
    #                                     functional_group=functional_group
    #                                )

    #     tissue, is_new_tissue = Tissue.objects.get_or_create(name=item['tissue_name'])
    #     protein.tissues.add(tissue)
    #     protein.save()


    #     dataset_item = DatasetItem(protein=protein, gene=item['gene_name'],
    #                                tissue=tissue, functional_group=functional_group,
    #                                family=family, species=item['species_name'],
    #                                dataset=dataset, peptide_sequence=item['sequence'],
    #                                molecular_weight=item['molecular_weight'],
    #                                tissue_weight_norm=item['tissue_weight_norm']
    #                    )
    #     dataset_item.save()

    # dataset.inserted_at = datetime.datetime.now()
    # dataset.is_inserted = True
    # dataset.save()

    # return HttpResponse(str(dataset.id))


@csrf_exempt
@login_required()
def dataset_upload(request):
    '''
    Uploads a file and inserts a dataset entry into the database
    '''
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
        file_delete_url = '/dataloader/datasets/delete/'
        file_insert_url = '/dataloader/datasets/insert/'

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
@login_required()
def dataset_uploadfiles(request):
    '''
    List of all datasets in the database.
    This is where insert and delete links are generated to be rendered
    on the data loader page. To display to display additional fields or links
    add them to the `item`
    '''

    datasets = Dataset.objects.all()
    result = {"files": []}
    for dataset in datasets:
        file_delete_url = '/dataloader/datasets/delete/'
        file_insert_url = '/dataloader/datasets/insert/'
        # file_delete_url = reverse('datasets-delete')
        # file_insert_url = reverse('datasets-insert')

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


@csrf_exempt
@login_required()
def dataloader(request):
    '''
    Backbone dataloader
    '''

    return render_to_response('dataloader.html')
