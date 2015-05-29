from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django import forms

import json

from itertools import chain

# Set of module names to exclude from view
EXCLUDE_MODULES = {"sites", "sessions", "contenttypes", "djcelery", "django", "south"}
EXCLUDE_MODULES = {}

class Cell(object):

    def __init__(self, text=""):
        self.attrs_dict = {}
        self.classes = []
        self.text = text

    def attr(self, *args, **kwargs):
        if kwargs:
            for key in kwargs:
                self.attrs_dict[key] = kwargs[key]
        elif args:
            return self.attrs_dict.get(args[0])

    def data(self, *args, **kwargs):
        for key in kwargs:
            data_key = "data-%s" % key
            self.attrs_dict[data_key] = kwargs[key]

    def render_attrs(self):
        self.attrs_dict["class"] = " ".join(self.classes)
        return " ".join(["{}='{}'".format(k, self.attrs_dict[k]) for k in self.attrs_dict])

    @property
    def html(self):
        return mark_safe("<td {}>{}</td>".format(self.render_attrs(), self.text))


class PermissionCell(Cell):

    def __init__(self, text="", has_perm=False):
        super(PermissionCell, self).__init__(text)
        self.classes.append("permission-cell")
        if has_perm:
            self.classes.append("perm_yes")


class PermNameCell(Cell):

    def __init__(self, text=""):
        super(PermNameCell, self).__init__(text)
        self.classes.append("permname")

    @property
    def html(self):
        return mark_safe("<td {}><span class='vertical-text'>{}</span></td>".format(self.render_attrs(), self.text))


class GroupPermissionForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    permission = forms.ModelChoiceField(queryset=Permission.objects.all())
    action = forms.ChoiceField(choices=(("add", "add"), ("remove", "remove")))

    def save(self):
        data = self.cleaned_data
        if data["action"] == "add":
            data["group"].permissions.add(data["permission"])
        else:
            data["group"].permissions.remove(data["permission"])

class PermissionMatrixView(View):

    def __init__(self):
        self.header_data = {}
        self.group_rows = []
        super(View, self).__init__()

    def get(self, request):
        """
        Render the main permission matrix view on template
        """
        self.build_headers(self.get_permissions())
        self.calculate_colspan()
        self.attach_groups()
        data = {
            "modules": list(self.all_modules()),  # Convert generator to list to allow reuse
            "models": self.all_models(),
            "permissions": self.all_permissions(),
            "groups": self.group_rows
        }
        return render(request, "permatrix/base.html", data)

    def post(self, request):
        data = json.loads(request.POST["data"])
        all_forms = [GroupPermissionForm(item) for item in data]
        if all(f.is_valid() for f in all_forms):
            for f in all_forms:
                f.save()
        else:
            return HttpResponse(status_code=300)

        return HttpResponse()

    def get_permissions(self):
        return Permission.objects.exclude(content_type__app_label__in=EXCLUDE_MODULES).select_related("content_type")

    def build_headers(self, permissions):
        # Assemble top row - modules
        for perm in permissions:
            app_label = perm.content_type.app_label
            if app_label not in self.header_data:
                cell = Cell(perm.content_type.app_label)
                cell.data(module=perm.content_type.app_label)
                self.header_data[app_label] = {"children": {}, "ct": perm.content_type, "cell": cell}
            app_container = self.header_data[app_label]
            model_name = perm.content_type.model
            if model_name not in app_container["children"]:
                cell = Cell(perm.content_type.name)
                cell.data(module=perm.content_type.app_label)
                app_container["children"][model_name] = {"children": {}, "ct": perm.content_type, "cell": cell}
            model_container = app_container["children"][model_name]
            full_name = "{}.{}".format(app_label, perm.codename)
            cell = PermNameCell(perm.codename)
            cell.data(module=perm.content_type.app_label)
            model_container["children"][perm.codename] = {"permission": perm, "groups": {}, "name": full_name, "cell": cell}

    def all_permissions(self):
        for model in self.all_models():
            for permission_name in sorted(model["children"]):
                yield model["children"][permission_name]

    def all_modules(self):
        for module_name in sorted(self.header_data):
            yield self.header_data[module_name]

    def all_models(self):
        for module in self.all_modules():
            for model_name in sorted(module["children"]):
                yield module["children"][model_name]

    def attach_groups(self):
        groups = Group.objects.all().order_by("name")
        for g in groups:
            data = {"group": g, "cells": []}
            permission_set = {perm.pk for perm in g.permissions.all()}
            for permission in self.all_permissions():
                cell = PermissionCell("", permission["permission"].pk in permission_set)
                cell.data(permission_id=permission["permission"].id, permission_name=permission["name"])
                cell.data(group_id=g.id, group_name=g.name)
                cell.data(module=permission["permission"].content_type.app_label)
                data["cells"].append(cell)
            self.group_rows.append(data)

    def calculate_colspan(self):
        for module in self.all_modules():
            for model in module["children"].values():
                model["cell"].attr(colspan=len(model["children"]))
            module["cell"].attr(colspan=sum(model["cell"].attr("colspan") for model in module["children"].values()))

