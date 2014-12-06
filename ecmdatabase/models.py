from django.db import models

# END_TODO

#temp
class Tissue(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

class Family(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

class FunctionalGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

import math
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
            norms = self.tissue_weight_norms.all().filter(tissue__name=t.name)
            average = math.fsum(norm.value for norm in norms)

            average = average / len(norms)
            all_average = all_average + average
            averages[t.name] = average

        all_average = all_average / len(self.tissues.all())
        averages['all'] = all_average
        return averages

class Dataset(models.Model):
    name = models.CharField(max_length=255, null=True)
    data_file = models.FileField(upload_to='datasets')
    is_inserted = models.BooleanField(default=False)
    inserted_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.name) + " (" + str(self.inserted_at) + ")"

class DatasetItem(models.Model):
    protein = models.ForeignKey(Protein)
    tissue = models.ForeignKey(Tissue)
    functional_group = models.ForeignKey(FunctionalGroup)
    family = models.ForeignKey(Family)
    species = models.CharField(max_length=255)

    dataset = models.ForeignKey(Dataset)

    peptide_sequence = models.TextField()
    gene = models.CharField(max_length=255)
    molecular_weight = models.FloatField()
    peptide_note = models.CharField(max_length=255)
    tissue_weight_norm = models.FloatField()

    def __str__(self):
        return str(self.dataset) + ": " + str(self.protein) + " " + str(self.tissue)