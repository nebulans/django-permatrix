#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from model_mommy import mommy

from permatrix.views import GroupPermissionForm


class PermissionFormTestCase(TestCase):

    def setUp(self):
        self.group = mommy.make("auth.Group")
        self.has_perm = mommy.make("auth.Permission")
        self.group.permissions.add(self.has_perm)
        self.not_perm = mommy.make("auth.Permission")

    def test_save_add(self):
        """
        Test saving form to add permission
        """
        f = GroupPermissionForm({
            "group": self.group.id,
            "permission": self.not_perm.id,
            "action": "add"
        })
        f.is_valid()
        f.save()
        result_ids = [i.id for i in self.group.permissions.all()]
        self.assertItemsEqual(result_ids, [self.has_perm.id, self.not_perm.id])

    def test_save_remove(self):
        """
        Test saving form to remove permission
        """
        f = GroupPermissionForm({
            "group": self.group.id,
            "permission": self.has_perm.id,
            "action": "remove"
        })
        f.is_valid()
        f.save()
        result_ids = [i.id for i in self.group.permissions.all()]
        self.assertItemsEqual(result_ids, [])

    def test_invalid_group(self):
        """
        Test that form is invalid for non-existent group id
        """
        g = mommy.make("auth.Group")
        g_id = g.id
        g.delete()
        f = GroupPermissionForm({
            "group": g_id,
            "permission": self.has_perm.id,
            "action": "add"
        })
        self.assertFalse(f.is_valid())

    def test_invalid_permission(self):
        """
        Test that form is invalid for non-existent permission id
        """
        p = mommy.make("auth.Permission")
        p_id = p.id
        p.delete()
        f = GroupPermissionForm({
            "group": self.group.id,
            "permission": p_id,
            "action": "add"
        })
        self.assertFalse(f.is_valid())

    def test_invalid_action(self):
        """
        Test that form is invalid for invalid action
        """
        f = GroupPermissionForm({
            "group": self.group.id,
            "permission": self.has_perm.id,
            "action": "invalid"
        })
        self.assertFalse(f.is_valid())

    def test_invalid_add(self):
        """
        Test that adding an existing permission raises a validation error
        """
        f = GroupPermissionForm({
            "group": self.group.id,
            "permission": self.has_perm.id,
            "action": "add"
        })
        self.assertFalse(f.is_valid())

    def test_invalid_remove(self):
        """
        Test that removing a non-existent permission raises a validation error
        """
        f = GroupPermissionForm({
            "group": self.group.id,
            "permission": self.not_perm.id,
            "action": "remove"
        })
        self.assertFalse(f.is_valid())