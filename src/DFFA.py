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

from src.models import TestTarget, TestCase
from src.utils import conf
from utils.utils import *


def get_uni_crash():
    pass


def push_file(local_path, file):
    push_cmd = ['adb', 'push', local_path + '/' + file, conf.REMOTE_PATH + file]
    popen_wait(push_cmd)


def rm_file(remote_file):
    '''
    清除文件
    '''
    rm_cmd = ['adb', 'shell', 'rm', conf.REMOTE_PATH + remote_file]
    popen_wait(rm_cmd)


def open_file(case):
    open_cmd = ['adb', 'shell', 'am', 'start', '-W', '-S']
    open_cmd.extend(['-a', case.target.action])
    open_cmd.extend(['-c', case.target.category])
    open_cmd.extend(['-t', case.target.mime_type])
    open_cmd.extend(['-d', 'file://' + conf.REMOTE_PATH + case.mutant_file])
    open_cmd.append(case.target.package + "/" + case.target.activity)
    print'执行:' + to_cmd_str(open_cmd)
    try:
        timeout_cmd(open_cmd, timeout=3)
    except TimeoutError as e:
        print e


def clean_log():
    log_clean_cmd = ['adb', 'logcat', '-c']
    print'执行:' + to_cmd_str(log_clean_cmd)
    popen_wait(log_clean_cmd)


def flush_log(case):
    log_cmd = ['adb', 'logcat', '-d', '-v', 'time', '*:E', '>',
               conf.LOG_PATH + '/' + 'log-' + case.mutant_file + '.txt']

    print'执行:' + to_cmd_str(log_cmd)
    popen_wait(log_cmd)


def run_job(cases, mutant_files_path, job_id):
    for i, case in enumerate(cases):
        print_symbol(i.__str__())
        # push变异文件
        push_file(mutant_files_path, case.mutant_file)
        # 清空日志
        clean_log()
        # 执行用例
        open_file(case)
        # 记录日志
        flush_log(case)
        # 删除变异文件
        rm_file(case.mutant_file)
        print_symbol('')


def run_jobs(target):
    format = 'png'
    job_path = conf.MUTANTS_PATH + '/' + format + '/'
    job_num = os.listdir(job_path).__len__()
    for i in range(1, job_num):
        mutant_files_path = job_path + i.__str__()
        mutant_files = os.listdir(mutant_files_path)

        cases = list()
        for file in mutant_files:
            cases.append(TestCase(target, file))
        run_job(cases, mutant_files_path, i)


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
    # target1 = TestTarget('com.alensw.PicFolder', 'com.alensw.transfer.TransferActivity',
    #                      'android.intent.action.SEND', 'android.intent.category.DEFAULT', 'image/*', 'foo', 'pic',
    #                      '11',
    #                      '22',
    #                      'test/')
    target = TestTarget('com.tencent.mm', 'com.tencent.mm.ui.tools.ShareScreenImgUI',
                        'android.intent.action.VIEW', 'android.intent.category.DEFAULT', 'image/*', 'foo', 'pic',
                        '11',
                        '22',
                        'test/')
    run_jobs(target)
