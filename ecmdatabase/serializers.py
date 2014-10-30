from ecmdatabase.models import Tissue, Protein, Experiment, ProteinHit, VariableModification
from rest_framework import serializers


class TissueSerializer(serializers.ModelSerializer):
    proteins = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Tissue
        fields = ('id', 'name', 'proteins')


class ProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ('id', 'long_gene_name', 'gene_name', 'prot_acc', 'name', 'tissue')

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
