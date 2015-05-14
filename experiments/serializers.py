from experiments.models import Experiment, Dataset, DatasetItem, RelativeConcentration
from rest_framework import serializers

class ExperimentSerializer(serializers.ModelSerializer):

    datasets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dataset_items = serializers.ListField(source='get_dataset_items')

    class Meta:
        model = Experiment
        fields = ('id', 'name', 'acquisition_date', 'species', 'data_type',
                  'acquisition_instrument', 'acquisition_type', 'publication',
                  'data_depository_link', 'slug', 'datasets', 'dataset_items')


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


class RelativeConcentrationSerializer(serializers.ModelSerializer):

    tissue_name = serializers.ReadOnlyField(source='tissue.name')

    class Meta:
        model = RelativeConcentration
        fields = ('id', 'sex', 'disease_state', 'disease_note', 'age',
                  'value', 'protein', 'tissue_name', 'dataset')

