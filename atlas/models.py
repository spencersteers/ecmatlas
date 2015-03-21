from django.db import models
from autoslug import AutoSlugField
import math


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
    gene_name                = models.CharField(max_length=255)
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
        for t in self.tissues.all():
            average = 0
            # queryset = TissueWeightNorm.objects.all()
            # queryset = queryset.filter(protein=self)
            # queryset = queryset.filter(tissue=tissue)
            items = self.dataset_items.all().filter(tissue=t)
            average = math.fsum(i.tissue_weight_norm for i in items)

            if len(items) < 1:
                average = 0
            else:
                average = average / len(items)

            all_average = all_average + average
            averages[t.name] = average

        all_average = all_average / len(self.tissues.all())
        averages['all'] = all_average
        return averages
