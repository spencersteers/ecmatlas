from django.db import models
from ecmdatabase.models import Protein, Tissue

class TissueWeightNorm(models.Model):
    '''
    Tissue weight norms from the dataset (per protein)
    '''
    # protein = models.ForeignKey(Protein, related_name='tissue_weight_norms')
    tissue = models.ForeignKey(Tissue)
    value = models.FloatField()

    def __str__(self):
        return str(self.protein.name) + " Tissue Weight Norm: " + str(value)