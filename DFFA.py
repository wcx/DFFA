#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
/*
 * Android framework fuzzer
 * Author: wcx
 * 对以文件为输入的Android APP 进行Fuzzing，收集错误信息，进行分类
 */

"""
import os

from transwarp.db import MySQLHelper
from utils.utils import *
from pretreatment.target import TestTarget


def push_files():
    '''
    向android devices push files
    '''
    local_path = 'files/pdfs'
    remote_path = '/mnt/sdcard/FuzzDownload'
    cmd = ['adb', 'push', local_path, remote_path]
    popen_wait(cmd)
    files = os.listdir(local_path)
    remote_files = [remote_path + '/' + file for file in files]
    return remote_files


def open_file(files):
    intent = 'android.intent.action.VIEW'
    mimetype = 'application/pdf'
    print(files)
    for file in files:
        print(file)
        data = 'file://' + file
        open_cmd = ['adb', 'shell', 'am', 'start', '-W', '-a',
                    intent, '-d', data, '-t', mimetype, 'cn.wps.moffice_eng']
        stop_cmd = ['adb', 'shell', 'am', 'force-stop', 'cn.wps.moffice_eng']
        popen_wait(open_cmd)
        popen_wait(stop_cmd)


def cleanup(files):
    '''
    清除文件
    '''
    rm_cmd = ['adb', 'shell', 'rm', '-r'] + files
    return popen_wait(rm_cmd)


def main():
    # 推送测试文件
    print_symbol("Start pushing")
    files = push_files()
    print(files)
    print_symbol("Done pushing")
    # 打开测试文件
    print_symbol("Start opening")
    open_file(files)
    print_symbol("Done opening")
    # 清除测试文件
    print_symbol("Start removing")
    print(files)
    cleanup(files)
    print_symbol("Done removing")


class TestCase(object):
    def __init__(self, target, mutant_file):
        self.target = target
        self.mutant_file = mutant_file


if __name__ == '__main__':
    sqlhelper = MySQLHelper()
    target = sqlhelper.query_target()
    sqlhelper.close()
    print target.activity
    case = TestCase(target, "file:///mnt/sdcard/Download/nexusx_1920x1080.png")
    cmd = ['adb', 'shell', 'am', 'start', '-W', '-a', 'android.intent.action.SEND_MULTIPLE', '-d', case.mutant_file,
           case.target.package + "/" + case.target.activity]
    print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    (stdoutput, erroutput) = p.communicate()
    # print stdoutput
    print erroutput
    stop_cmd = ['adb', 'shell', 'am', 'force-stop', 'com.alensw.PicFolder']
    subprocess.Popen(stop_cmd)
    # adb
    # shell
    # am
    # start - W - a
    # android.intent.action.SEND_MULTIPLE - d
    # file: // / mnt / sdcard / Download / nexusx_1920x1080.png - c
    # android.intent.category.DEFAULT
    # com.alensw.PicFolder / com.alensw.transfer.TransferActivity
