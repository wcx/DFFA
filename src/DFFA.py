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
from src.models import TestTarget, TestCase, Device
from src.pretreatment.pretreatment import parse_apks
from src.utils import conf
from utils.utils import *


class DFFA(object):
    adb_cmd = ['adb', '-s']
    log_path = conf.LOG_PATH

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
        print'执行:' + to_cmd_str(open_cmd)
        timeout_cmd(open_cmd, timeout=3)

    def clean_log(self):
        log_clean_cmd = self.adb_cmd + (['logcat', '-c'])
        print'执行:' + to_cmd_str(log_clean_cmd)
        popen_wait(log_clean_cmd)

    def flush_log(self, case):
        log_cmd = self.adb_cmd + (['logcat', '-d', '-v', 'time', '*:E', '>',
                                   self.log_path + '/' + 'log-' + case.mutant_file + '.txt'])

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
        # 指定设备
        self.adb_cmd.extend([device.serialno])
        self.log_path += '/' + device.serialno
        mkdirs(self.log_path)
        # 选择测试目标
        targets = self.select_targets()
        for target in targets:
            # 检查目标APP是否安装,未安装则进行安装
            self.install_apk(target)
            # 开始运行测试用例
            self.run_jobs(target)

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
            if content.__len__() > 1:
                if content[1] == 'device\n':
                    device = Device()
                    device.serialno = content[0]
                    device.brand = self.getprop(device, 'brand')
                    device.model = self.getprop(device, 'model')
                    device.build_id = self.getprop(device, 'build_id')
                    device.version_release = self.getprop(device, 'version_release')
                    devices.append(device)
        print '当前可用设备' + str(devices.__len__()) + '台'
        for d in devices:
            print d.serialno + '\t' + d.brand + '\t' + d.model + '\t' + d.build_id + '\t' + d.version_release
        return devices

    def run_devices(self):
        devices = self.list_devices()
        if devices.__len__() == 0:
            print '未连接Android设备,程序退出'
        else:
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
    # dffa.list_devices()
