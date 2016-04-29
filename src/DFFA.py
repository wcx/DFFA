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

from src.pretreatment.target import TestTarget
from transwarp.db import MySQLHelper
from utils.utils import *

RES_PATH='..+/res'
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


if __name__ == '__main__':
    # sqlhelper = MySQLHelper()
    # target = sqlhelper.query_target()
    # sqlhelper.close()

    target = TestTarget('com.alensw.PicFolder', 'com.alensw.transfer.TransferActivity', '*/*', 'foo', 'pic', '11', '22',
                        'test/')
    mutant_file = "file:///mnt/sdcard/Download/nexusx_1920x1080.png"
    case = TestCase(target, mutant_file)

    open_cmd = ['adb', 'shell', 'am', 'start', '-W', '-S']
    open_cmd.extend(['-a', 'android.intent.action.SEND_MULTIPLE'])
    open_cmd.extend(['-t', 'image/*'])
    open_cmd.extend(['-d', case.mutant_file])
    open_cmd.append(case.target.package + "/" + case.target.activity)

    log_clean_cmd = ['adb', 'logcat', '-c']
    print'执行:' + to_cmd_str(log_clean_cmd)
    p1 = subprocess.Popen(to_cmd_str(log_clean_cmd), shell=True)
    p1.wait()

    print'执行:' + to_cmd_str(open_cmd)
    try:
        timeout_cmd(to_cmd_str(open_cmd), timeout=3)
    except TimeoutError as e:
        print e
        # subprocess.Popen(to_cmd_str(open_cmd),shell=True)

    log_cmd = ['adb', 'logcat', '-d', '-v', 'time', '*:E', '>', '../res/logs/log.txt']
    print'执行:' + to_cmd_str(log_cmd)
    subprocess.Popen(to_cmd_str(log_cmd), shell=True)
