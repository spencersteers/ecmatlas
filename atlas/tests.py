from django.test import TestCase
from atlas.models import Protein
from atlas.serializers import ProteinSerializer

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

import pprint


class ProteinTests(APITestCase):

    fixtures = ['tissue.json', 'protein.json', 'tissueweightnorm.json']

    def test_list(self):
        url = reverse('protein-list')
        response = self.client.get(url)
        p = Protein.objects.all()
        self.assertEquals(response.data["count"], len(p))

    def test_detail(self):
        url = reverse('protein-detail', args=[1])
        response = self.client.get(url)
        self.assertEquals(1,1)
