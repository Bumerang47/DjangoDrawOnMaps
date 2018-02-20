# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase


class IndexPageTests(TestCase):
    """
    Testes for load home page
    """

    def test_list_view(self):
        # tet available home page
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)