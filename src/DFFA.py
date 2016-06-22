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

from src import conf
from src.pretreatment.models import TestTarget
from transwarp.db import MySQLHelper
from utils.utils import *


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


def get_uni_crash():
    pass


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


def push_mutant_file(local_path):
    pass


def run_campaign(cases):
    for i, case in enumerate(cases):
        local_path = FILES_PATH + '/job1' + cases.mutant_file
        remote_path = '/mnt/sdcard/FuzzDownload'
        push_cmd = ['adb', 'push', local_path, remote_path]

        print_symbol(i.__str__())
        open_cmd = ['adb', 'shell', 'am', 'start', '-W', '-S']
        open_cmd.extend(['-a', case.target.action])
        open_cmd.extend(['-c', case.target.category])
        open_cmd.extend(['-t', case.target.mime_type])
        open_cmd.extend(['-d', case.mutant_file])
        open_cmd.append(case.target.package + "/" + case.target.activity)
        # 清空日志
        log_clean_cmd = ['adb', 'logcat', '-c']
        print'执行:' + to_cmd_str(log_clean_cmd)
        popen_wait(log_clean_cmd)
        # 执行用例
        print'执行:' + to_cmd_str(open_cmd)
        try:
            timeout_cmd(open_cmd, timeout=3)
        except TimeoutError as e:
            print e
        # 记录日志
        log_cmd = ['adb', 'logcat', '-d', '-v', 'time', '*:E', '>',
                   '../res/logs/' + 'log' + time.time().__str__() + '.txt']
        print'执行:' + to_cmd_str(log_cmd)
        popen_wait(log_cmd)
        print_symbol()


if __name__ == '__main__':
    # sqlhelper = MySQLHelper()
    # target = sqlhelper.query_target()
    # sqlhelper.close()

    # target = TestTarget('com.alensw.PicFolder', 'com.alensw.transfer.TransferActivity',
    #                     'android.intent.action.SEND_MULTIPLE', 'android.intent.category.DEFAULT', 'image/*', 'foo',
    #                     'pic',
    #                     '11',
    #                     '22',
    #                     'test/')
    mutant_file = 'file:///mnt/sdcard/Download/nexusx_1920x1080.png'
    target = TestTarget('com.alensw.PicFolder', 'com.alensw.transfer.TransferActivity',
                        'android.intent.action.SEND', 'android.intent.category.DEFAULT', 'image/*', 'foo', 'pic',
                        '11',
                        '22',
                        'test/')
    format = 'png'
    job_path = conf.MUTANTS_PATH + '/' + format + '/'
    job_num = os.listdir(job_path).__len__()
    for i in range(1, 2):
        cases = os.listdir(job_path+i.__str__())
        for case in cases:
            push_file()
            print case


    push_mutant_files()
    cases = list()
    # for file in files:
    #     cases.append(TestCase(target, 'file://mnt/sdcard/Download/' + file))
    # print cases.__len__()
    # run_campaign(cases)
