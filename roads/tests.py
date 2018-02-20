# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
import json
from models import Roads, Azs
from django.test import TestCase


class RoadsTests(TestCase):
    """
    Testes for Road model and get list
    """

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.road_data = [[43.67752, 43.5098],
                         [43.67783, 43.5099]]

    @classmethod
    def create_road(self, road_code=10024, name="Nalchik",
                    length_km=2014.5, geomtype='LineString', coordinates=list()):
        if len(coordinates) == 0:
            coordinates = self.road_data
        try:
            resp_rd = Roads.objects.get(road_code=road_code)
        except Roads.DoesNotExist:
            resp_rd = Roads.objects.create(
                road_code=road_code, name=name, length_km=length_km,
                geomtype=geomtype, coordinates=coordinates)
        return resp_rd

    def test_create_model(self):
        r = self.create_road()
        self.assertTrue(isinstance(r, Roads))

    def test_list_view(self):
        # Simple view test
        r = self.create_road()
        url = reverse("roads_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        j_resp = json.loads(resp.json())
        self.assertTrue(len(j_resp) > 0)
        self.assertIn('coordinates', j_resp[0])
        self.assertTrue(len(j_resp[0]['coordinates']) > 0)


class AzsTests(TestCase):
    """
    Testes for Azs model and get list
    """

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.coord_data = [[43.67752, 43.5098],
                          [43.67783, 43.5099]]

    @classmethod
    def create_road(self, road_code=10024, name="Nalchik",
                    length_km=2014.5, geomtype='LineString', coordinates=list()):
        # Create temp object road for testes

        if len(coordinates) == 0:
            coordinates = self.coord_data
        try:
            resp_rd = Roads.objects.get(road_code=road_code)
        except Roads.DoesNotExist:
            resp_rd = Roads.objects.create(
                road_code=road_code, name=name, length_km=length_km,
                geomtype=geomtype, coordinates=coordinates)
        return resp_rd

    @classmethod
    def create_azs(self, road, geomtype='Point', coordinates=list()):
        # Create temp object azs for testes

        if len(coordinates) == 0:
            coordinates = self.coord_data
        azs = Azs.objects.create(
            road_code=road, geomtype=geomtype, coordinates=coordinates)
        return azs

    def test_create_model(self):
        # Test create Azs object

        road = self.create_road()
        azs = self.create_azs(road)
        self.assertTrue(isinstance(azs, Azs))

    def test_azs_of_road(self):
        # Tet get azs of road

        road = self.create_road()
        azs = self.create_azs(road)
        azs.road = road
        url = reverse('road_of_azs', args=(road.road_code,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        j_resp = json.loads(resp.json())
        self.assertTrue(len(j_resp) > 0)
        self.assertIn('coordinates', j_resp[0])
        self.assertTrue(len(j_resp[0]['coordinates']) > 0)
