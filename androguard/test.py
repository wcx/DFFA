#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

from androguard.core.bytecodes import apk
from testcase import Testcase

apk_path = "/home/wcx/Download/apk/kuaituliulan_4722404.apk"
apkf = apk.APK(apk_path)
print apkf.get_app_name()
print apkf.get_androidversion_code()
print apkf.get_androidversion_name()
print apkf.get_package()
print apkf.get_filename()
print apkf.get_type()

testcase = Testcase(apkf.get_package(), apkf.get_main_activity(), "video/*", apkf.get_filename(), apkf.get_app_name(),
                    apkf.get_androidversion_code(), apkf.get_androidversion_name())
print testcase.get_package_name()
