from django.db import models
from django_extensions.db.fields import AutoSlugField

from collections import defaultdict
import math
import requests


class Tissue(models.Model):

    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return str(self.name)


class Family(models.Model):

    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return str(self.name)


class FunctionalGroup(models.Model):

    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return str(self.name)


class Protein(models.Model):
    '''
    This is the proteins' common data among all experiments
    '''

    sequence                 = models.TextField()
    gene_name                = models.CharField(max_length=255, unique=True)
    protein_name             = models.CharField(max_length=255, null=True)
    species                  = models.CharField(max_length=255, null=True)
    tissues                  = models.ManyToManyField(Tissue, related_name='proteins', null=True)
    family                   = models.ForeignKey(Family, null=True)
    functional_group         = models.ForeignKey(FunctionalGroup, null=True)
    slug                     = AutoSlugField(populate_from='gene_name')

    def __str__(self):
        return str(self.sequence) + ": " + str(self.protein_name)

    def get_average_tissue_weight_norms(self):
        averages = dict()
        all_average = 0
        atwn = self.average_tissue_weight_norms.all()
        if len(atwn) < 1:
            return

        for norm in atwn:
            averages[norm.tissue.name] = norm.average
            all_average += norm.average

        all_average = all_average / len(atwn)
        averages['all'] = all_average
        return averages

    def get_average_relative_concentrations(self):
        averages = defaultdict(list)

        arc = self.average_relative_concentrations.all()
        if len(arc) < 1:
            return

        for a in arc:
            averages[a.tissue.name].append({'tissue_state': a.tissue_state, 'average': a.average})
        
        return averages

class ProteinExternalReference(models.Model):
    protein = models.OneToOneField(Protein, related_name='external_reference')
    wikipedia_summary = models.TextField(null=True)
    wikipedia_id = models.CharField(max_length=255, null=True)
    wikipedia_url = models.URLField(null=True)
    uniprot_id = models.CharField(max_length=255, null=True)
    uniprot_url = models.URLField(null=True)

    @classmethod
    def create_from_protein(cls, protein):
        from celery.utils.log import get_task_logger
        logger = get_task_logger(__name__)
        reference = cls(protein=protein)

        # fetch and set wikipedia information
        wikipedia_json = cls.get_wikipedia_for_gene(protein.gene_name)
        try:
            wikipedia_id = list(wikipedia_json.keys())[0]
            if int(wikipedia_id) > 0:
                categories = wikipedia_json[wikipedia_id]['categories']
                for cat in categories:
                    pprint.pprint(cat)
                    if 'disambiguation' in cat['title'].lower():
                        raise Exception('disambiguation page')
                reference.wikipedia_id = wikipedia_id
                reference.wikipedia_summary = wikipedia_json[wikipedia_id]['extract']
                reference.wikipedia_url = 'http://en.wikipedia.org/?curid={}'.format(wikipedia_id)
            else:
                logger.info("Wikipedia not found for Protein {}".format(protein.gene_name))
        except:
            logger.error("Error adding wikipedia reference for Protein {}".format(protein.gene_name))
            pass

        # fetch and set uniprot information
        uniprot_id = cls.get_uniprot_for_gene(protein.gene_name)
        if uniprot_id:
            reference.uniprot_id = uniprot_id
            reference.uniprot_url = 'http://www.uniprot.org/uniprot/{}'.format(uniprot_id)
        else:
            logger.info("Error adding uniprot reference for Protein {}".format(protein.gene_name))
        return reference

    @classmethod
    def get_wikipedia_for_gene(cls, gene_name):
        search_title = gene_name
        request_params = { 'action': 'query', 'titles': search_title, 'prop': 'categories|extracts', 'exintro': '', 'redirects': '', 'format': 'json'}
        r = requests.get('http://en.wikipedia.org/w/api.php', params=request_params)
        json_response = r.json()['query']['pages']
        return json_response

    @classmethod
    def get_uniprot_for_gene(cls, gene_name):
        request_params = { 'action': 'query', 'titles': str(gene_name), 'prop': 'extracts', 'exintro': '', 'redirects': '', 'format': 'json'}
        uni_response = requests.get('http://www.uniprot.org/uniprot/?query=gene:'+str(gene_name)+'&format=tab')
        if len(uni_response.text):
            my_lines = str(uni_response.text).split('\n')
            uni_id = my_lines[1].split('\t')
            return uni_id[0]
        else:
            return None