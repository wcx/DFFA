#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from androguard.core.bytecodes import apk

apk_path = "/home/wcx/Download/apk/kuaituliulan_4722404.apk"
apkf = apk.APK(apk_path)
print apkf.get_main_activity()
print apkf.get_app_name()
print apkf.get_elements("data", "mimeType")
print apkf.get_type()

