# -*- coding: utf-8 -*-
import zipfile
import axmlprinter
from axmlprinter import AXMLPrinter
from xml.dom import minidom


NS_ANDROID_URI = 'http://schemas.android.com/apk/res/android'
apk_path = "/home/wcx/Download/apk/kuaituliulan_4722404.apk"
z = zipfile.ZipFile(apk_path, 'r')
for f in z.namelist():
    if f == "AndroidManifest.xml":
        ap = axmlprinter.AXMLPrinter(z.read(f))
        buff = minidom.parseString(ap.getBuff()).toxml()
        print buff
        xml = minidom.parseString(AXMLPrinter(z.read(f)).getBuff())
        print("packagename"+xml.documentElement.getAttribute("package"))
        print(xml.documentElement.getAttribute("android:versionCode"))
        print(xml.documentElement.getAttribute("android:versionName"))
        # x = set()
        # y = set()
        # for item in xml.getElementsByTagName("activity"):
        #     for sitem in item.getElementsByTagName("action"):
        #         val = sitem.getAttributeNS(NS_ANDROID_URI, "name")
        #         if val == "android.intent.action.MAIN":
        #             x.add(item.getAttributeNS(NS_ANDROID_URI, "name"))

        #     for sitem in item.getElementsByTagName("category"):
        #         val = sitem.getAttributeNS(NS_ANDROID_URI, "name")
        #         if val == "android.intent.category.LAUNCHER":
        #             y.add(item.getAttributeNS(NS_ANDROID_URI, "name"))

        # z = x.intersection(y)
        # if len(z) > 0:
        #     print z.pop()
        for item in xml.getElementsByTagName("activity"):
            for sitem in item.getElementsByTagName("intent-filter"):
                for ssitem in sitem.getElementsByTagName("data"):
                    val = ssitem.getAttributeNS(NS_ANDROID_URI, "mimeType")
                    if val == "image/*":
                        print "activity:"+item.getAttributeNS(NS_ANDROID_URI, "name")
                        print "type:"+val
                        print "--------------------------------------------------------------------------------"
