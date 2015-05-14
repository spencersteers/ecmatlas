from django.db import models
from django_extensions.db.fields import AutoSlugField
from atlas.models import Tissue, Family, FunctionalGroup, Protein


class Experiment(models.Model):

    name = models.CharField(max_length=255, null=True)
    acquisition_date = models.DateField(null=True)
    species = models.CharField(max_length=255, null=True)
    data_type = models.CharField(max_length=255, null=True)
    acquisition_instrument = models.CharField(max_length=255, null=True)
    acquisition_type = models.CharField(max_length=255, null=True)
    publication = models.URLField(null=True)
    data_depository_link = models.CharField(max_length=255, null=True)
    slug = AutoSlugField(populate_from='get_full_name')

    def __str__(self):
        return str(self.name)

    def get_full_name():
        return '{} {}'.format(str(self.name), str(self.acquisition_date))


    def get_dataset_items(self):
        dataset_items = []
        datasets = self.datasets.all()
        for dataset in datasets:
            dataset_items.append(dataset.dataset_items.all().values_list('id', flat=True))

        return dataset_items[0]



class Dataset(models.Model):

    name = models.CharField(max_length=255, null=True)
    data_file = models.FileField(upload_to='uploads/datasets')
    is_inserted = models.BooleanField(default=False)
    inserted_at = models.DateTimeField(null=True)
    experiment = models.ForeignKey(Experiment, null=True, related_name='datasets')

    def __str__(self):
        return str(self.name) + " (" + str(self.inserted_at) + ")"

from django.dispatch import receiver
@receiver(models.signals.post_delete, sender=Dataset)
def handle_deleted_dataset(sender, instance, **kwargs):

    if instance.experiment.datasets.count() is 0:
        instance.experiment.delete()


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
    protein = models.ForeignKey(Protein, related_name='relative_concentrations')
    tissue = models.ForeignKey(Tissue)
    dataset = models.ForeignKey(Dataset)
    experiment = models.ForeignKey(Experiment, related_name='relative_concentrations')

    def get_tissue_with_state_name(self):
        name = self.tissue.name
        if self.disease_note:
            name += " - " + self.disease_note

        return name
        

class AverageRelativeConcentration(models.Model):

    protein = models.ForeignKey(Protein, related_name='average_relative_concentrations')
    tissue_state = models.CharField(max_length=255, null=True)
    tissue = models.ForeignKey(Tissue, null=True)
    average = models.FloatField(null=True)


class AverageTissueWeightNorm(models.Model):

    protein = models.ForeignKey(Protein, related_name='average_tissue_weight_norms')
    tissue = models.ForeignKey(Tissue, null=True)
    average = models.FloatField(null=True)