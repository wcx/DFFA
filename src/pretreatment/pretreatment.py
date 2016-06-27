#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('../../')
reload(sys)
sys.setdefaultencoding('utf8')

import os

from src.pretreatment.androguard.core.bytecodes import apk
from src.transwarp.db import MySQLHelper
from src.models import TestTarget, IntentFilter

BASE_SEED_PATH = "../../res/seeds"


def get_attributes(sitem, tag, attribute):
    s = set()
    for ssitem in sitem.getElementsByTagName(tag):
        val = ssitem.getAttributeNS(apk.NS_ANDROID_URI, attribute)
        if val != '':
            s.add(val)
    return s


def get_target_mime(mime_types):
    target_mime = set()
    for t in mime_types:
        if t.startswith("image/") or t.startswith("video/") or t.startswith("*/"):
            if t == "image/*":
                target_mime.add("image/gif")
                target_mime.add("image/jpg")
                target_mime.add("image/png")
            elif t == "video/*":
                target_mime.add("video/mp3")
                target_mime.add("video/mp4")
            elif t == "*/*":
                target_mime.add("image/gif")
                target_mime.add("image/jpg")
                target_mime.add("image/png")
                target_mime.add("video/mp3")
                target_mime.add("video/mp4")
            elif t == "image/gif" or t == "image/jpg" or t == "image/png" or t == "video/mp3" or t == "video/mp4":
                target_mime.add(t)
    return target_mime


def get_mime_types(apkf):
    d = dict()
    for i in apkf.xml:
        for j, item in enumerate(apkf.xml[i].getElementsByTagName("activity")):
            activity = item.getAttributeNS(apk.NS_ANDROID_URI, "name")
            for sitem in item.getElementsByTagName("intent-filter"):
                actions = get_attributes(sitem, "action", "name")
                categorys = get_attributes(sitem, "category", "name")
                mime_types = get_target_mime(get_attributes(sitem, "data", "mimeType"))
                # 添加activity以及对应的mime types
                if mime_types:
                    d.update({apkf.format_value(activity): IntentFilter(actions, categorys, mime_types)})
                    print "activity:" + apkf.format_value(
                        activity) + "\ntypes:" + mime_types.__str__() + "\nactions:" + actions.__str__() + "\ncategory:" + categorys.__str__()
                    print "-------"
        print "activity number:" + len(d).__str__() + "||||" + d.__str__()
    return d


def get_seed(mime_type):
    if mime_type == "image/gif":
        seed = BASE_SEED_PATH + "input.gif"
    if mime_type == "image/jpg":
        seed = BASE_SEED_PATH + "input.jpg"
    if mime_type == "image/png":
        seed = BASE_SEED_PATH + "input.png"
    if mime_type == "video/mp3":
        seed = BASE_SEED_PATH + "input.mp3"
    if mime_type == "video/mp4":
        seed = BASE_SEED_PATH + "input.mp4"
    return os.path.realpath(seed)


def to_targets(apk_path):
    apkf = apk.APK(apk_path)
    print "------------------appname:" + apkf.get_app_name() + "---------------------"
    # 转换为TestTarget,并放入集合
    print "---开始---分析mime type---"
    d = get_mime_types(apkf)
    print "---结束---分析mime type---"
    targets = set()
    print "---开始---target convert---"
    for activity in d:
        intent_filter = d[activity]
        for mime_type in intent_filter.mime_types:
            seed = get_seed(mime_type)
            for action in intent_filter.actions:
                for category in intent_filter.categorys:
                    targets.add(
                        TestTarget(apkf.get_package(), activity, action, category, mime_type,
                                   os.path.realpath(apkf.get_filename()),
                                   apkf.get_app_name(),
                                   apkf.get_androidversion_code(), apkf.get_androidversion_name(),
                                   seed))

    print "---结束---target convert---"
    return targets


def parse_apk(apk_path, sqlhelper):
    targets = to_targets(apk_path)
    print "---开始---存入数据库----"
    sqlhelper.insert_targets(targets)
    print "---结束---存入数据库----"


def parse_apks(base_path):
    sqlhelper = MySQLHelper()
    sqlhelper.init()
    local_path = base_path
    files = os.listdir(local_path)

    apk_paths = []
    for f in files:
        if f.endswith('.apk'):
            apk_paths.append(local_path + '/' + f)

    print "----------------------------------共" + len(apk_paths).__str__() + "个待解析APK------------------------------"
    for i, path in enumerate(apk_paths):
        print "-----------------开始解析第" + str(i + 1) + "个APK:" + path + "----------------------"
        parse_apk(path, sqlhelper)
        print "-----------------结束解析第" + str(i + 1) + "个APK:" + path + "----------------------\n"
    sqlhelper.close()


if __name__ == '__main__':
    parse_apks('../../res/apks')
    # apkf = apk.APK('/home/wcx/Download/apk/04d7098dc1c6268c870d0b20aa881bfe.apk')
    # print apkf.get_app_name()
    # sqlhelper = MySQLHelper()
    # parse_apk('/home/wcx/Download/apk/04d7098dc1c6268c870d0b20aa881bfe.apk', sqlhelper)
    # sqlhelper.close()
