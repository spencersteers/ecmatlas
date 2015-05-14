from __future__ import absolute_import

from celery import shared_task

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import json
import requests
import datetime
import pytz
import re
import math
from collections import defaultdict

from experiments.models import Experiment, Dataset, DatasetItem, RelativeConcentration, AverageTissueWeightNorm, AverageRelativeConcentration
from atlas.models import Tissue, Family, FunctionalGroup, Protein, ProteinExternalReference
from dataloader import parser

@shared_task
def parse_dataset(dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)
    file_path = dataset.data_file.path

    logger.info("parsing dataset {} ...".format(dataset_id))
    result = parser.parse_dataset(file_path)

    logger.info("creating models ...")
    ### save experiment model
    experiment_results = result['experiment']
    date = re.findall('(\d{8})', experiment_results['name'])
    acquisition_date = None
    if len(date) > 0:
        acquisition_date = datetime.datetime.strptime(date[0], '%Y%m%d') # 20141117
        acquisition_date = acquisition_date.replace(tzinfo=pytz.UTC)
        experiment_results['name'] = (experiment_results['name'].replace(date[0], '')).strip()
    experiment, is_new_experiment = Experiment.objects.get_or_create(name=experiment_results['name'],
                                                  species=experiment_results['species'],
                                                  data_type=experiment_results['data_type'],
                                                  acquisition_instrument=experiment_results['acquisition_instrument'],
                                                  publication=experiment_results['publication'],
                                                  data_depository_link=experiment_results['data_depository_link'],
                                                  acquisition_date=acquisition_date
                                                )
    experiment.save()


    dataset.experiment = experiment
    dataset.inserted_at = datetime.datetime.now(pytz.utc)
    dataset.is_inserted = True
    dataset.save()

    new_proteins = []
    dataset_items = []
    ### save new dataset_item models
    # print(result['dataset_items'])
    for item in result['dataset_items']:
        family, is_new_family = Family.objects.get_or_create(name=item['family_name'])
        functional_group, is_new_fg = FunctionalGroup.objects.get_or_create(name=item['functional_group_name'])

        protein = None
        try:
            protein = Protein.objects.get(gene_name=item['gene_name'])
        except Protein.DoesNotExist:
            protein = Protein(sequence=item['sequence'], gene_name=item['gene_name'],
                            protein_name=item['protein_name'], species=item['species_name'],
                            family=family, functional_group=functional_group
                      )
            protein.save()
            new_proteins.append(protein)

        tissue, is_new_tissue = Tissue.objects.get_or_create(name=item['tissue_name'])
        tissue.save()
        protein.tissues.add(tissue)
        protein.save()

        try:
            float_value = float(item['tissue_weight_norm'])
        except ValueError:
            continue
            pass

        dataset_item = DatasetItem(protein=protein, gene=item['gene_name'],
                                   tissue=tissue, functional_group=functional_group,
                                   family=family, species=item['species_name'],
                                   dataset=dataset, peptide_sequence=item['sequence'],
                                   molecular_weight=item['molecular_weight'],
                                   tissue_weight_norm=item['tissue_weight_norm']
                       )
        dataset_item.save()
        dataset_items.append(dataset_item)


    concentrations = []
    ### save new concentrations models
    # print(result['concentrations'])
    #{'disease_note': 'normal', 'disease_state': 'C0', 'time_point': '0', 'sample_identifier': 'MU0092', 
    # 'gene': 'VWF', 'fraction': '3', 'age': '27', 'tissue': 'Placenta', 'sex': 'm ', 'value': '1.60E+08'}
    for concentration in result['concentrations']:
        # skip values we can't cast to float
        float_value = float()
        try:
            float_value = float(concentration['value'])
        except ValueError:
            # logger.info('str to float ValueError: {}'.format(concentration['value']))
            pass

        protein, is_new_protein = Protein.objects.get_or_create(
                                        gene_name=concentration['gene'],
                                   )
        if is_new_protein:
            new_proteins.append(protein)

        tissue, is_new_tissue = Tissue.objects.get_or_create(name=concentration['tissue'])
        tissue.save()
        protein.tissues.add(tissue)
        protein.save()

        relative_concentration, is_new_concentration = RelativeConcentration.objects.get_or_create(
                                                                sex=concentration['sex'],
                                                                disease_state=concentration['disease_state'],
                                                                disease_note=concentration['disease_note'],
                                                                age=concentration['age'],
                                                                value=float_value,
                                                                protein=protein,
                                                                tissue=tissue,
                                                                dataset=dataset,
                                                                experiment=experiment
                                                       )
        relative_concentration.save()
        concentrations.append(relative_concentration)

    process_average_tissue_weight_norms.delay(dataset_id)
    process_average_relative_concentrations.delay(dataset_id)
    process_external_references.delay(new_proteins)

    return None


@shared_task
def process_external_references(proteins):
    logger.info("processing external references ...")
    for protein in proteins:
        reference = ProteinExternalReference.create_from_protein(protein)
        reference.save()
    logger.info("{0} external references added".format(len(proteins)))
    return None


@shared_task
def process_average_tissue_weight_norms(dataset_id):
    logger.info("processing tissue weight norms ...")

    dataset = Dataset.objects.get(pk=dataset_id)
    proteins = Protein.objects.all()

    
    for p in proteins:
        averages = dict()
        all_average = 0
        for t in p.tissues.all():
            average = 0
            items = p.dataset_items.all().filter(tissue=t)
            average = math.fsum(i.tissue_weight_norm for i in items)

            if len(items) < 1:
                continue
            
            average = average / len(items)

            all_average = all_average + average
            averages[t.name] = average

        for tissue_name in averages:
            t = Tissue.objects.get(name=tissue_name)
            atwn = AverageTissueWeightNorm(protein=p, tissue=t, average=averages[tissue_name])
            atwn.save()


    logger.info("{0} protein average tissue weight norms calculated".format(len(proteins)))
    return None

from collections import defaultdict

@shared_task
def process_average_relative_concentrations(dataset_id):
    logger.info("processing relative concentrations...")

    dataset = Dataset.objects.get(pk=dataset_id)
    
    proteins = Protein.objects.all()
    averages = defaultdict(list)

    for p in proteins:
        concentrations = RelativeConcentration.objects.filter(protein=p)
        if len(concentrations) < 1:
            continue
        
        for c in concentrations:
            averages[c.get_tissue_with_state_name()].append(c.value)
        
        for tissue_name in averages:
            t_name = tissue_name.split('-')[0].strip()
            t = Tissue.objects.get(name=t_name)
            average = sum(averages[tissue_name]) / len(averages[tissue_name])
            arc, is_new = AverageRelativeConcentration.objects.get_or_create(protein=p, tissue_state=tissue_name, tissue=t)
            arc.average = average
            arc.save()

    logger.info("{0} protein average relative concentrations calculated".format(len(proteins)))
    return None