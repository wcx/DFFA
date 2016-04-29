#!/usr/bin/env python
# -*- coding: utf-8 -*


class TestTarget(object):
    def __init__(self, package, activity, mime_type, file_name, app_name, version_code, version_name, seed):
        self.package = package
        self.activity = activity
        self.file_name = file_name
        self.mime_type = mime_type
        self.app_name = app_name
        self.version_code = version_code
        self.version_name = version_name
        self.seed = seed

        # @property
        # def package(self):
        #     return self.package
        #
        # @property
        # def activity(self):
        #     return self.activity
        #
        # @property
        # def file_name(self):
        #     return self.file_name
        #
        # @property
        # def mime_type(self):
        #     return self.mime_type
        #
        # @property
        # def app_name(self):
        #     return self.app_name
        #
        # @property
        # def version_code(self):
        #     return self.version_code
        #
        # @property
        # def version_name(self):
        #     return self.version_name
        #
        # @property
        # def seeds(self):
        #     return self.seeds


if __name__ == '__main__':
    target = TestTarget("com.test", "com.test.act", "*/*", "/sd/a/a.jpg", "piuk", "123", "1.01", "~/")
    print target.mime_type
