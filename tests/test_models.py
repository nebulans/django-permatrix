#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-permatrix
------------

Tests for `django-permatrix` models module.
"""

from django.test import TestCase

from permatrix.views import PermissionMatrixView

class TestPermatrix(TestCase):

    def setUp(self):
        pass

    # def test_all_modules_sorted(self):
    #     PMV = PermissionMatrixView()
    #     PMV.header_data = {"alpha": "first", "gamma": "last", "beta": "second"}
    #     result = [x for x in PMV.all_modules()]
    #     self.assertEqual(result, ["first", "second", "last"])

    def tearDown(self):
        pass
