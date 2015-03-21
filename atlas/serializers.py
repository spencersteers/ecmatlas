from atlas.models import Tissue, Family, FunctionalGroup, Protein
from rest_framework import serializers


class TissueSerializer(serializers.ModelSerializer):

    proteins = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tissue
        fields = ('id', 'name', 'slug', 'proteins')


class FamilySerializer(serializers.ModelSerializer):

    class Meta:
        model = Family
        fields = ('id', 'name', 'slug')


class FunctionalGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = FunctionalGroup
        fields = ('id', 'name', 'slug')


class ProteinSerializer(serializers.ModelSerializer):

    average_tissue_weight_norms = serializers.DictField(source='get_average_tissue_weight_norms')
    family_name = serializers.ReadOnlyField(source='family.name')
    functional_group_name = serializers.ReadOnlyField(source='functional_group.name')

    class Meta:
        model = Protein
        fields = ('id', 'sequence', 'gene_name', 'protein_name', 'species',
                  'tissues', 'family_name', 'functional_group_name', 'slug',
                  'average_tissue_weight_norms')
