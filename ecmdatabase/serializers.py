from ecmdatabase.models import Tissue, Family, FunctionalGroup, Protein, Dataset, DatasetItem
from rest_framework import serializers


class TissueSerializer(serializers.ModelSerializer):
    proteins = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tissue
        fields = ('id', 'name', 'proteins')


class FamilySerializer(serializers.ModelSerializer):

    class Meta:
        model = Family
        fields = ('id', 'name')

class FunctionalGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = FunctionalGroup
        fields = ('id', 'name')

class ProteinSerializer(serializers.ModelSerializer):
    average_tissue_weight_norms = serializers.DictField(source='get_average_tissue_weight_norms')
    family_name = serializers.ReadOnlyField(source='family.name')
    functional_group_name = serializers.ReadOnlyField(source='functional_group.name')
    class Meta:
        model = Protein
        fields = ('id', 'sequence', 'gene_name', 'protein_name', 'species', 'tissues', 'family_name', 'functional_group_name', 'average_tissue_weight_norms')


class DatasetSerializer(serializers.ModelSerializer):
    dataset_items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    name =  serializers.ReadOnlyField(source='data_file.url')
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'inserted_at', 'dataset_items')

class DatasetItemSerializer(serializers.ModelSerializer):
    family_name = serializers.ReadOnlyField(source='family.name')
    functional_group_name = serializers.ReadOnlyField(source='functional_group.name')
    tissue_name = serializers.ReadOnlyField(source='tissue.name')
    class Meta:
        model = DatasetItem
        fields = ('id', 'protein', 'tissue_name', 'functional_group_name', 'family_name', 'species', 'dataset', 'peptide_sequence', 'gene', 'molecular_weight', 'tissue_weight_norm')