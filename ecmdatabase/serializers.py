from ecmdatabase import Protein
from rest_framework import serializers


class ProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ('long_gene_name', 'gene_name', 'prot_acc', 'name')
