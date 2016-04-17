#!/usr/bin/env python
# -*- coding: utf-8 -*


class TestTarget(object):
    def __init__(self, package, activity, file_type, file_name, app_name, version_code, version_name):
        self.package = package
        self.activity = activity
        self.file_name = file_name
        self.file_type = file_type
        self.app_name = app_name
        self.version_code = version_code
        self.version_name = version_name

    def get_package_name(self):
        return self.package

    def set_package_name(self, package):
        self.package = package
