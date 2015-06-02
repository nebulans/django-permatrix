#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from permatrix.views import PermissionMatrixView


class TestViewGenerators(TestCase):
    """
    Test the generators in the PermissionMatrixView for correctly ordered output
    """

    HEADER_DATA = {
        "admin": {
            "children": {
                "group": {
                    "children": {
                        "add_group": "add_group"
                    }
                },
                "permission": {
                    "children": {
                        "add_permission": "add_permission",
                        "delete_permission": "delete_permission"
                    }
                },
                "user": {
                    "children": {
                        "add_user": "add_user"
                    }
                }
            }
        },
        "blog": {
            "children": {
                "author": {
                    "children": {
                        "add_author": "add_author",
                        "change_author": "change_author",
                        "delete_author": "delete_author",
                        "approve_author": "approve_author"
                    },
                },
                "post": {
                    "children": {
                        "add_post": "add_post",
                    },
                },
                "tag": {
                    "children": {
                        "add_tag": "add_tag",
                        "change_tag": "change_tag",
                        "delete_tag": "delete_tag",
                        "merge_tag": "merge_tag"
                    }
                }
            }
        }
    }

    def test_all_modules_sorted(self):
        """
        Test that the all modules generator returns items in the correct sorted order
        """
        PMV = PermissionMatrixView()
        PMV.header_data = self.HEADER_DATA
        result = [x for x in PMV.all_modules()]
        self.assertEqual(result, [self.HEADER_DATA[i] for i in ["admin", "blog"]])

    def test_all_models_sorted(self):
        """
        Test that the all models generator returns models sorted first
        by module then by model
        """
        PMV = PermissionMatrixView()
        PMV.header_data = self.HEADER_DATA
        result = [x for x in PMV.all_models()]
        expected = [("admin", "group"), ("admin", "permission"), ("admin", "user"), ("blog", "author"), ("blog", "post"), ("blog", "tag")]
        self.assertEqual(result, [self.HEADER_DATA[i[0]]["children"][i[1]] for i in expected])

    def test_all_permissions_sorted(self):
        """
        Test that the all_permissions generator returns permissions sorted
        by module then model then permission
        """
        PMV = PermissionMatrixView()
        PMV.header_data = self.HEADER_DATA
        result = [x for x in PMV.all_permissions()]
        expected = ["add_group", "add_permission", "delete_permission", "add_user", "add_author", "approve_author",
                    "change_author", "delete_author", "add_post", "add_tag", "change_tag", "delete_tag", "merge_tag"]
        self.assertEqual(result, expected)

    def test_all_modules_stable(self):
        PMV = PermissionMatrixView()
        PMV.header_data = self.HEADER_DATA
        results = [list(PMV.all_modules()) for i in range(10)]
        for i in results:
            self.assertEqual(results[0], i)

    def test_all_models_stable(self):
        PMV = PermissionMatrixView()
        PMV.header_data = self.HEADER_DATA
        results = [list(PMV.all_models()) for i in range(10)]
        for i in results:
            self.assertEqual(results[0], i)

    def test_all_permissions_stable(self):
        PMV = PermissionMatrixView()
        PMV.header_data = self.HEADER_DATA
        results = [list(PMV.all_permissions()) for i in range(10)]
        for i in results:
            self.assertEqual(results[0], i)