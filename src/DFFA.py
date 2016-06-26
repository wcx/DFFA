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

from src.fuzzer import fuzz_file
from src.models import TestTarget, TestCase
from src.pretreatment.pretreatment import parse_apks
from src.utils import conf
from utils.utils import *


def list_devices():
    devices = list()
    return devices


class DFFA(object):
    adb_cmd = ['adb', '-s']

    def get_uni_crash(self):
        pass

    def push_file(self, local_path, file):
        push_cmd = self.adb_cmd + (['push', local_path + '/' + file, conf.REMOTE_PATH + file])
        popen_wait(push_cmd)

    def rm_file(self, remote_file):
        '''
        清除文件
        '''
        rm_cmd = self.adb_cmd + (['shell', 'rm', conf.REMOTE_PATH + remote_file])
        popen_wait(rm_cmd)

    def open_file(self, case):
        open_cmd = self.adb_cmd + (['shell', 'am', 'start', '-W', '-S'])
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

    def clean_log(self):
        log_clean_cmd = self.adb_cmd + (['logcat', '-c'])
        print'执行:' + to_cmd_str(log_clean_cmd)
        popen_wait(log_clean_cmd)

    def flush_log(self, case):
        log_cmd = self.adb_cmd + (['logcat', '-d', '-v', 'time', '*:E', '>',
                                   conf.LOG_PATH + '/' + 'log-' + case.mutant_file + '.txt'])

        print'执行:' + to_cmd_str(log_cmd)
        popen_wait(log_cmd)

    def is_install(self, target):
        check_cmd = self.adb_cmd + (['shell', 'pm', 'list', 'package', '|', 'grep', '-c', target.package])
        p = popen_wait(check_cmd)
        return p.stdout.readline()

    def install_apk(self, target):
        install_cmd = self.adb_cmd + (['install', target.file_name])
        if not self.is_install(target):
            popen_wait(install_cmd)

    def run_job(self, cases, mutant_files_path, job_id):
        for i, case in enumerate(cases):
            print_symbol(str(i))
            # push变异文件
            self.push_file(mutant_files_path, case.mutant_file)
            # 清空日志
            self.clean_log()
            # 执行用例
            self.open_file(case)
            # 记录日志
            self.flush_log(case)
            # 删除变异文件
            self.rm_file(case.mutant_file)
            print_symbol('')

    def run_jobs(self, target):
        format = target.mime_type.split('/')[1]
        job_path = conf.MUTANTS_PATH + '/' + format + '/'
        if os.path.exists(job_path):
            job_num = os.listdir(job_path).__len__()
            for i in range(1, job_num):
                mutant_files_path = job_path + str(i)
                mutant_files = os.listdir(mutant_files_path)

                cases = list()
                for file in mutant_files:
                    cases.append(TestCase(target, file))
                self.run_job(cases, mutant_files_path, i)
        else:
            print '没有对应变异文件,程序退出:\n' + format + ' files didn\'t exist'

    def select_targets(self):
        # sqlhelper = MySQLHelper()
        # target = sqlhelper.query_target()
        # sqlhelper.close()
        targets = list()
        target = TestTarget('com.tencent.mm', 'com.tencent.mm.ui.tools.ShareScreenImgUI',
                            'android.intent.action.VIEW', 'android.intent.category.DEFAULT', 'image/png', 'foo', 'pic',
                            '11',
                            '22',
                            'test/')
        targets.append(target)
        return targets

    def run_targets(self, device):
        self.adb_cmd.extend([str(device)])
        # 选择测试目标
        targets = self.select_targets()
        for target in targets:
            # 检查目标APP是否安装,未安装则进行安装
            self.install_apk(target)
            # 开始运行测试用例
            self.run_jobs(target)

    def run_devices(self):
        devices = list_devices()
        devices.append('8XV5T15A20015305')
        for device in devices:
            self.run_targets(device)

    def fuck(self):
        self.run_devices()


if __name__ == '__main__':
    # 解析apk
    # parse_apks(conf.APK_PATH)
    # 生成测试文件
    # fuzz_file(seedfile='../res/seeds/Lenna.png', job_num=10, job_case_num=3)
    # 进行测试
    dffa = DFFA()
    dffa.fuck()
