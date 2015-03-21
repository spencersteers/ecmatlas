from django.db import models
from atlas.models import Tissue, Family, FunctionalGroup, Protein


# class Experiment(models.Model):
#     pass


class Dataset(models.Model):

    name = models.CharField(max_length=255, null=True)
    data_file = models.FileField(upload_to='uploads/datasets')
    is_inserted = models.BooleanField(default=False)
    inserted_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.name) + " (" + str(self.inserted_at) + ")"


class DatasetItem(models.Model):

    protein = models.ForeignKey(Protein, related_name='dataset_items')
    tissue = models.ForeignKey(Tissue)
    functional_group = models.ForeignKey(FunctionalGroup)
    family = models.ForeignKey(Family)
    species = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dataset, related_name='dataset_items')
    peptide_sequence = models.TextField()
    gene = models.CharField(max_length=255)
    molecular_weight = models.FloatField()
    peptide_note = models.CharField(max_length=255)
    tissue_weight_norm = models.FloatField()

    def __str__(self):
        return str(self.dataset) + ": " + str(self.protein) + " " + str(self.tissue)
