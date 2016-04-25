#!/usr/bin/env python
# -*- coding: utf-8 -*


class TestTarget(object):
    def __init__(self, package, activity, mime_type, file_name, app_name, version_code, version_name, seed):
        self._package = package
        self._activity = activity
        self._file_name = file_name
        self._mime_type = mime_type
        self._app_name = app_name
        self._version_code = version_code
        self._version_name = version_name
        self._seed = seed

    @property
    def package(self):
        return self._package

    @property
    def activity(self):
        return self._activity

    @property
    def file_name(self):
        return self._file_name

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def app_name(self):
        return self._app_name

    @property
    def version_code(self):
        return self._version_code

    @property
    def version_name(self):
        return self._version_name

    @property
    def seed(self):
        return self._seed


if __name__ == '__main__':
    target = TestTarget("com.test", "com.test.act", "*/*", "/sd/a/a.jpg", "piuk", "123", "1.01", "~/")
    print target.mime_type
