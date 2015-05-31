#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from permatrix.views import Cell, PermissionCell, PermNameCell

class CellTestCase(TestCase):

    def test_text(self):
        """
        Test setting of cell text in constructor
        """
        t = "Test Text"
        c = Cell(t)
        self.assertEqual(c.text, t)

    def test_attr_setting_one(self):
        """
        Test setting of a single HTML attribute via the attr method
        """
        c = Cell()
        c.attr(somekey="someval")
        self.assertEqual(c.attrs_dict["somekey"], "someval")

    def test_attr_setting_multiple(self):
        """
        Test setting of multiple HTML attributes via the attr method
        """
        c = Cell()
        c.attr(somekey="someval", anotherkey="anotherval")
        self.assertEqual(c.attrs_dict["somekey"], "someval")
        self.assertEqual(c.attrs_dict["anotherkey"], "anotherval")

    def test_attr_overwriting(self):
        """
        Test overwriting of attributes via the attr method
        """
        c = Cell()
        c.attr(key="firstval")
        c.attr(key="secondval")
        self.assertEqual(c.attrs_dict["key"], "secondval")

    def test_attr_access(self):
        """
        Test accessing already stored attributes via the attr method
        """
        c = Cell()
        c.attr(key="val")
        self.assertEqual(c.attr("key"), "val")

    def test_data_setting_one(self):
        """
        Test setting of one HTML data attribute via the data method
        """
        c = Cell()
        c.data(key="val")
        self.assertEqual(c.attrs_dict["data-key"], "val")

    def test_data_setting_multiple(self):
        """
        Test setting multiple HTML data attributes via the data method
        """
        c = Cell()
        c.data(key="val", foo="bar")
        self.assertEqual(c.attrs_dict["data-key"], "val")
        self.assertEqual(c.attrs_dict["data-foo"], "bar")

    def test_data_overwriting(self):
        """
        Test overwriting of data attributes via the data method
        """
        c = Cell()
        c.data(key="initial")
        c.data(key="final")
        self.assertEqual(c.attrs_dict["data-key"], "final")

    def test_data_access(self):
        """
        Test accessing data attributes via the data method
        """
        c = Cell()
        c.data(key="val")
        self.assertEqual(c.data("key"), "val")

    def test_render_attrs_one(self):
        """
        Test rendering a single attribute into HTML form
        """
        c = Cell()
        c.attr(key="val")
        self.assertEqual(c.render_attrs(), "key='val'")

    def test_render_attrs_multiple(self):
        """
        Test that multiple attributes get correctly delineated
        """
        c = Cell()
        c.attr(key="val", foo="bar")
        possibles = ("key='val' foo='bar'", "foo='bar' key='val'")
        self.assertTrue(c.render_attrs() in possibles)

    def test_class_rendering_one(self):
        """
        Test rendering of a single class into an HTML attribute
        """
        c = Cell()
        c.classes.append("foo")
        self.assertEqual(c.render_attrs(), "class='foo'")

    def test_class_rendering_multiple(self):
        """
        Test rendering of multiple classes into HTML attributes
        """
        c = Cell()
        c.classes.append("foo")
        c.classes.append("bar")
        self.assertEqual(c.render_attrs(), "class='foo bar'")

    def test_html_output_empty(self):
        """
        Test the skeleton output for no input
        """
        c = Cell()
        self.assertEqual(c.html, "<td ></td>")

    def test_html_output_text(self):
        """
        Test HTML output of the cell text
        """
        c = Cell("Title")
        self.assertEqual(c.html, "<td >Title</td>")

    def test_html_output_attrs(self):
        """
        Test that the HTML output contains the attrs as rendered
        """
        c = Cell()
        c.data(foo="bar")
        self.assertEqual(c.html, "<td %s></td>" % c.render_attrs())


class PermissionCellTestCase(TestCase):

    def test_no_perm(self):
        """
        Test correct classes for no permission on perm cell
        """
        c = PermissionCell(has_perm=False)
        self.assertEqual(c.classes, ["permission-cell"])

    def test_has_perm(self):
        """
        Test correct classes for has perm on perm cell
        """
        c = PermissionCell(has_perm=True)
        self.assertEqual(c.classes, ["permission-cell", "perm_yes"])

    def test_no_text(self):
        """
        Test that cell text is empty string for no text input
        """
        c = PermissionCell()
        self.assertEqual(c.text, "")

    def test_has_text(self):
        """
        Test cell text passed through correctly
        """
        c = PermissionCell(text="Some Title")
        self.assertEqual(c.text, "Some Title")


class PermNameCellTestCase(TestCase):

    def test_classes(self):
        """
        Test that correct classes are attached to cell
        """
        c = PermNameCell()
        self.assertEqual(c.classes, ["permname"])

    def test_no_text(self):
        """
        Test cell text is empty string for no text passed
        """
        c = PermNameCell()
        self.assertEqual(c.text, "")

    def test_text_passed(self):
        """
        Test cell text passed correctly
        """
        c = PermNameCell("Some Header")
        self.assertEqual(c.text, "Some Header")

    def test_html_output(self):
        """
        Test cell html output
        """
        c = PermNameCell("TEXT")
        self.assertEqual(c.html, "<td class='permname'><span class='vertical-text'>TEXT</span></td>")