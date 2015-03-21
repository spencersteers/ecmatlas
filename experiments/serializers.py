from experiments.models import Dataset, DatasetItem
from rest_framework import serializers


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
        fields = ('id', 'protein', 'tissue_name', 'functional_group_name',
                  'family_name', 'species', 'dataset', 'peptide_sequence',
                  'gene', 'molecular_weight', 'tissue_weight_norm')
