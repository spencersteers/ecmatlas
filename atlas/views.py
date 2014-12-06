from atlas.models import TissueWeightNorm
from atlas.serializers import TissueWeightNormSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import math

@api_view(['GET',])
def tissueweightnorm_average(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        queryset = TissueWeightNorm.objects.all()

        protein = request.QUERY_PARAMS.get('protein', None)
        tissue = request.QUERY_PARAMS.get('tissue', None)

        if protein is not None:
            queryset = queryset.filter(protein=protein)
        if tissue is not None:
            queryset = queryset.filter(tissue=tissue)

        average = math.fsum(norm.value for norm in queryset)

        average = average / len(queryset)
        return Response(average)