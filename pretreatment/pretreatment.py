#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('../../')

import os
from androguard.core.bytecodes import apk
from androguard.target import TestTarget
from transwarp.db import MySQLHelper

def get_mime_types(apkf):
    d = dict()
    for i in apkf.xml:
        for j, item in enumerate(apkf.xml[i].getElementsByTagName("activity")):
            activity = item.getAttributeNS(apk.NS_ANDROID_URI, "name")
            mime_types = set()
            for sitem in item.getElementsByTagName("intent-filter"):
                for ssitem in sitem.getElementsByTagName("data"):
                    val = ssitem.getAttributeNS(apk.NS_ANDROID_URI, "mimeType")
                    if val != '':
                        mime_types.add(val)
            # 添加activity以及对应的mime types
            if mime_types:
                print "activity:" + activity + "||||types:" + mime_types.__str__()
                d.update({activity: mime_types})
        print "activity number:" + str(len(d)) + "||||" + d.__str__()
    return d


def to_targets(apk_path):
    apkf = apk.APK(apk_path)
    # 转换为TestTarget,并放入集合
    print "---开始---分析mime type---"
    d = get_mime_types(apkf)
    print "---结束---分析mime type---"
    targets = set()
    print "---开始---target convert---"
    for activity in d:
        for mime_type in d[activity]:
            targets.add(TestTarget(apkf.get_package(), activity, mime_type, apkf.get_filename(), apkf.get_app_name(),
                                   apkf.get_androidversion_code(), apkf.get_androidversion_name()))
    print "---结束---target convert---"
    return targets


def to_sql(targets, sqlhelper):
    for target in targets:
        sqlhelper.insert(sqlhelper.TABLE_TARGET, vars(target))


def parse_apk(apk_path, sqlhelper):
    print "---开始---解析APK----"
    targets = to_targets(apk_path)
    print "---结束---解析APK----"
    print "---开始---存入数据库----"
    to_sql(targets, sqlhelper)
    print "---结束---存入数据库----"


def parse_apks():
    sqlhelper = MySQLHelper()
    local_path = '/home/wcx/Download/apk'
    files = os.listdir(local_path)
    apk_paths = [local_path + '/' + f for f in files]
    print apk_paths.__str__()
    for path in apk_paths:
        parse_apk(path, sqlhelper)
    sqlhelper.close()


if __name__ == '__main__':
    parse_apks()
