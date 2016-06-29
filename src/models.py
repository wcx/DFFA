#!/usr/bin/env python
# -*- coding: utf-8 -*


class TestTarget(object):
    id = 0

    def __init__(self, package, activity, action, category, mime_type, file_name, app_name, version_code, version_name,
                 seed):
        self.package = package
        self.activity = activity
        self.action = action
        self.category = category
        self.mime_type = mime_type
        self.file_name = file_name
        self.app_name = app_name
        self.version_code = version_code
        self.version_name = version_name
        self.seed = seed

    def __str__(self):
        s = ''
        for name, value in vars(self).items():
            s += '%s=%s|' % (name, value)
        return s


class IntentFilter(object):
    def __init__(self, actions=[], categorys=[], mime_types=[]):
        self.actions = actions
        self.categorys = categorys
        self.mime_types = mime_types


class TestCase(object):
    def __init__(self, target, mutant_file):
        self._target = target
        self._mutant_file = mutant_file

    @property
    def target(self):
        return self._target

    @property
    def mutant_file(self):
        return self._mutant_file

    @mutant_file.setter
    def mutant_file(self, value):
        self._mutant_file = value

    @target.setter
    def target(self, value):
        self._target = value


class Device(object):
    serialno = ''
    version_release = ''
    model = ''
    brand = ''
    build_id = ''


if __name__ == '__main__':
    target = TestTarget("com.test", "com.test.act", "*/*", "/sd/a/a.jpg", "*/*", "/sd/a/a.jpg", "piuk", "123", "1.01",
                        "~/")
    target.id = 0
    print target.__str__()
