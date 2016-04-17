#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('../../')
reload(sys)
sys.setdefaultencoding('utf8')
import os
from androguard.core.bytecodes import apk
from target import TestTarget
from transwarp.db import MySQLHelper

BASE_APK_PATH = "/home/wcx/Download/apk"


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
    print "------------------name:"+apkf.get_app_name()+"---------------------"
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
    targets = to_targets(apk_path)
    print "---开始---存入数据库----"
    to_sql(targets, sqlhelper)
    print "---结束---存入数据库----"


def parse_apks(base_path):
    sqlhelper = MySQLHelper()
    local_path = base_path
    files = os.listdir(local_path)
    apk_paths = [local_path + '/' + f for f in files]
    print "----------------------------------共" + len(apk_paths).__str__() + "个待解析APK------------------------------"
    for i, path in enumerate(apk_paths):
        print "-----------------开始解析第" + str(i + 1) + "个APK:" + path + "----------------------"
        parse_apk(path, sqlhelper)
        print "-----------------结束解析第" + str(i + 1) + "个APK:" + path + "----------------------\n"
    sqlhelper.close()


if __name__ == '__main__':
    parse_apks(BASE_APK_PATH)
    # apkf = apk.APK('/home/wcx/Download/apk/04d7098dc1c6268c870d0b20aa881bfe.apk')
    # print apkf.get_app_name()
    # sqlhelper = MySQLHelper()
    # parse_apk('/home/wcx/Download/apk/04d7098dc1c6268c870d0b20aa881bfe.apk', sqlhelper)
    # sqlhelper.close()
