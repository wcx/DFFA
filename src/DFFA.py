#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
/*
 * Android framework fuzzer
 * Author: wcx
 * 对以文件为输入的Android APP 进行Fuzzing，收集错误信息，进行分类
 */

"""
import sys

from src import conf
from src.fuzzer import fuzz_file
from src.models import TestCase, Device
from src.pretreatment.pretreatment import parse_apks
from src.transwarp.db import MySQLHelper
from utils.utils import *


class DFFA(object):
    adb_cmd = ['adb', '-s']
    log_path = ''
    installed_apk = set()
    CUSTOM_JOB_NUM = 0

    def get_uni_crash(self):

        pass

    def push_file(self, local_path, file):
        push_cmd = self.adb_cmd + (['push', local_path + '/' + file, conf.REMOTE_PATH + file])
        popen_wait(push_cmd)

    def rm_file(self, remote_file):
        """
        删除文件
        :param remote_file: 文件名称
        :return:
        """
        rm_cmd = self.adb_cmd + (['shell', 'rm', conf.REMOTE_PATH + remote_file])
        popen_wait(rm_cmd)

    def open_file(self, case):
        open_cmd = self.adb_cmd + (['shell', 'am', 'start', '-W', '-S'])
        open_cmd.extend(['-a', case.target.action])
        open_cmd.extend(['-c', case.target.category])
        open_cmd.extend(['-t', case.target.mime_type])
        open_cmd.extend(['-d', 'file://' + conf.REMOTE_PATH + case.mutant_file])
        open_cmd.append(case.target.package + "/" + case.target.activity)
        timeout_cmd(open_cmd, is_print=True)

    def clean_log(self):
        log_clean_cmd = self.adb_cmd + (['logcat', '-c'])
        popen_wait(log_clean_cmd)

    def flush_log(self, case):
        log_cmd = self.adb_cmd + (['logcat', '-d', '-v', 'time', 'AndroidRuntime:E', '*:S'])
        p = popen_wait(log_cmd)
        log = p.stdout.readlines()
        if log.__len__() < 4:
            print 'no bug'
        else:
            with open(self.log_path + '/' + case.mutant_file.split('.')[0], 'w') as log_file:
                log_file.writelines(log)
                print log
                # for line in p.stdout.readlines():

    def run_job(self, cases, mutant_files_path, job_id):
        for i, case in enumerate(cases):
            print_symbol('target id-' + str(case.target.id) + '\t' + str(case.target.app_name) + '\tcase id-' + str(
                job_id) + '-' + str(i + 1))
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
            print_symbol()

    @log_runtime
    def run_jobs(self, target):
        format = target.mime_type.split('/')[1]
        job_path = conf.MUTANTS_PATH + '/' + format + '/'
        if os.path.exists(job_path):
            if self.CUSTOM_JOB_NUM < 1:
                job_num = os.listdir(job_path).__len__() - 1
            else:
                job_num = self.CUSTOM_JOB_NUM
            print '执行任务数为' + str(job_num)
            for job_id in range(1, job_num):
                mutant_files_path = job_path + str(job_id)
                mutant_files = os.listdir(mutant_files_path)

                cases = list()

                for file in mutant_files:
                    cases.append(TestCase(target, file))
                self.run_job(cases, mutant_files_path, job_id)
        else:
            print '没有对应变异文件,程序退出:\n' + format + ' files didn\'t exist'
            sys.exit()

    def select_targets(self, num=0):
        sqlhelper = MySQLHelper()
        targets = sqlhelper.query_targets_by_type('image/png', num)
        sqlhelper.close()

        print_after_symbol('选择的target有:')
        for target in targets:
            print_before_symbol(target.__str__())
        return targets

    def is_install(self, package):
        print 'checking target ' + package
        check_cmd = self.adb_cmd + (['shell', 'pm', 'list', 'package', '|', 'grep', '-c', package])
        p = popen_wait(check_cmd)
        result = p.stdout.readline().strip()
        return int(result)

    def install_apks(self, targets):
        packages = set()
        for target in targets:
            packages.add(target.package)

        for package in packages:
            if package not in self.installed_apk:
                if not self.is_install(package):
                    install_cmd = self.adb_cmd + (['install', package])
                    print 'installing ' + package
                    popen_wait(install_cmd)
                    self.installed_apk.add(package)
        print_in_symbol('已安装apk:' + str(self.installed_apk))

    def uninstall_apks(self, targets):
        for target in targets:
            if target.package in self.installed_apk:
                uninstall_cmd = self.adb_cmd + (['uninstall', target.package])
                print 'uninstalling ' + target.app_name
                popen_wait(uninstall_cmd)
                self.installed_apk.remove(target.package)

    def run_targets(self, device):
        # 选择测试目标
        targets = self.select_targets()
        # 检查目标APP是否安装,未安装则进行安装
        self.install_apks(targets)
        for i, target in enumerate(targets):
            # 开始运行测试用例
            if self.is_install(target.package):
                self.log_path = conf.LOG_PATH + '/' + device.serialno + '/target-' + str(target.id)
                mkdirs(self.log_path)
                print_after_symbol('Fuzzing target-' + str(target.id))
                self.run_jobs(target)
            else:
                print '{0}未安装,进入下一个target'.format(target.app_name.strip())
            logs = os.listdir(self.log_path)
            if len(logs) == 0:
                os.removedirs(self.log_path)

        self.uninstall_apks(targets)
        return targets

    def getprop(self, device, key):
        """
        获取设备信息
        :param device:
        :param key: 需获取属性
        :return: 从设备获取的属性
        """
        tmp = ''
        if key == 'brand':
            tmp = 'ro.product.brand'
        elif key == 'model':
            tmp = 'ro.product.model'
        elif key == 'build_id':
            tmp = 'ro.build.id'
        elif key == 'version_release':
            tmp = 'ro.build.version.release'
        else:
            return tmp

        get_prop_cmd = ['adb', '-s', str(device.serialno), 'shell', 'getprop', tmp]
        p = popen_wait(get_prop_cmd)
        result = p.stdout.readline()
        return result.strip()

    def list_devices(self):
        """
        列出可用设备
        :return: Device对象列表
        """
        devices = list()
        list_cmd = ['adb', 'devices']
        p = popen_wait(list_cmd)
        for line in p.stdout.readlines():
            content = line.split('\t')
            if len(content) > 1:
                if content[1] == 'device\n':
                    device = Device()
                    device.serialno = content[0]
                    device.brand = self.getprop(device, 'brand')
                    device.model = self.getprop(device, 'model')
                    device.build_id = self.getprop(device, 'build_id')
                    device.version_release = self.getprop(device, 'version_release')
                    devices.append(device)
        print '当前可用设备' + str(len(devices)) + '台'
        for d in devices:
            print d.serialno + '\t' + d.brand + '\t' + d.model + '\t' + d.build_id + '\t' + d.version_release
        print_symbol()
        return devices

    def run_devices(self):
        devices = self.list_devices()
        if len(devices) == 0:
            print '未连接Android设备,程序退出'
            sys.exit()
        else:
            for device in devices:
                # 指定设备
                self.adb_cmd.extend([device.serialno])
                self.run_targets(device)

    def fuzzing(self):
        self.run_devices()


if __name__ == '__main__':
    # 解析apk
    # parse_apks(conf.APK_PATH)
    # 生成测试文件
    # fuzz_file(seedfile='/home/wcx/Development/Research/DFFA/res/seeds/Lenna.png', job_num=2, job_case_num=1)
    # 进行测试
    dffa = DFFA()
    dffa.fuzzing()
