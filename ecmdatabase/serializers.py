from ecmdatabase.models import Tissue, Protein, Experiment, ProteinHit, VariableModification
from atlas.serializers import TissueWeightNormSerializer
from rest_framework import serializers


class TissueSerializer(serializers.ModelSerializer):
    proteins = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Tissue
        fields = ('id', 'name', 'proteins')


class ProteinSerializer(serializers.ModelSerializer):
    average_tissue_weight_norms = serializers.Field(source='get_average_tissue_weight_norms')
    class Meta:
        model = Protein
        fields = ('id', 'sequence', 'gene_name', 'protein_name', 'species', 'tissues', 'average_tissue_weight_norms')

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        #fields =


class ProteinHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProteinHit
        #fields = ('id', 'long_gene_name', 'gene_name', 'prot_acc', 'name', 'tissue')


class VariableModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableModification
        #fields = ('id', 'long_gene_name', 'gene_name', 'prot_acc', 'name', 'tissue')
