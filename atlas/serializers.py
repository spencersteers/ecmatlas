from atlas.models import TissueWeightNorm
from rest_framework import serializers


class TissueWeightNormSerializer(serializers.ModelSerializer):

    class Meta:
        model = TissueWeightNorm
        fields = ('id', 'protein', 'tissue', 'value')