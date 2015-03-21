from django.db import models
from atlas.models import Tissue, Family, FunctionalGroup, Protein


class Experiment(models.Model):

    name = models.CharField(max_length=255, null=True)
    aquisition_date = models.DateField(null=True)
    species = models.CharField(max_length=255, null=True)
    data_type = models.CharField(max_length=255, null=True)
    aquisition_instrument = models.CharField(max_length=255, null=True)
    aquisition_type = models.CharField(max_length=255, null=True)
    publication = models.URLField(null=True)
    data_depository_link = models.CharField(max_length=255, null=True)
    slug = AutoSlugField(populate_from='get_full_name')

    def __str__(self):
        return str(self.name)

    def get_full_name():
        return str(self.name) + str(self.aquisition_date)


class Dataset(models.Model):

    name = models.CharField(max_length=255, null=True)
    data_file = models.FileField(upload_to='uploads/datasets')
    is_inserted = models.BooleanField(default=False)
    inserted_at = models.DateTimeField(null=True)
    experiment = models.ForeignKey(Experiment)

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


class RelativeConcentration(models.Model):

    sex = models.CharField(max_length=255, null=True)
    disease_state = models.CharField(max_length=255, null=True)
    disease_note = models.CharField(max_length=255, null=True)
    age = models.IntegerField(null=True)
    value = models.FloatField()
    protein = models.ForeignKey(Protein)
    tissue = models.ForeignKey(Tissue)
    dataset = models.ForeignKey(Dataset)

