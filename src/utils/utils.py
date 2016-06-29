#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
import subprocess
import time
from datetime import timedelta


def home_screen():
    return send_key_event('3')


def send_key_event(event_num):
    cmd = ['adb', 'shell', 'input', 'keyevent', event_num]
    popen_wait(cmd)


def print_symbol(string=''):
    print("---------------------------------------" + string +
          "---------------------------------------------------")


def print_before_symbol(string, message=''):
    print string
    print_symbol(string=message)


def print_in_symbol(string, message=''):
    print_symbol(string=message)
    print string
    print_symbol(string=message)


def print_after_symbol(string, message=''):
    print_symbol(string=message)
    print string


def to_cmd_str(cmd):
    """
    # 格式化命令
    e.g ['adb','shell','list']->adb shell list
    :param cmd:
    :return:
    """
    return ' '.join(str(i) for i in cmd)


class TimeoutError(Exception):
    pass


def popen_wait(cmd, is_print=False):
    cmd = to_cmd_str(cmd)
    if is_print:
        print cmd
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    p.wait()
    return p


def timeout_cmd(cmd, timeout=5):
    """
    执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    :param cmd: 要执行的命令
    :param timeout: 最长等待时间，单位：秒
    :return:
    """
    cmd = ['timeout', str(timeout)] + cmd
    popen_wait(cmd)


# def timeout_cmd(cmd, timeout=60):
#     """
#     执行命令cmd，返回命令输出的内容。
#     如果超时将会抛出TimeoutError异常。
#     :param cmd: 要执行的命令
#     :param timeout: 最长等待时间，单位：秒
#     :return:
#     """
#     cmd = to_cmd_str(cmd)
#     p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
#     t_beginning = time.time()
#     seconds_passed = 0
#     while True:
#         if p.poll() is not None:
#             break
#         seconds_passed = time.time() - t_beginning
#         if timeout and seconds_passed > timeout:
#             p.terminate()
#             raise TimeoutError(cmd, timeout)
#         time.sleep(0.1)
#     return p


def log_runtime(function):
    """
    包装方法,显示方法运行时间
    :param function:
    :return:
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        start_localtime = time.localtime()
        print '[%s()] is starting.' % function.__name__
        ####
        rst = function(*args, **kwargs)
        ####
        end = time.time()
        print time.strftime("%Y-%m-%d %H:%M:%S", start_localtime)
        print '[%s()] is end.' % function.__name__
        run_time = end - start
        print str(timedelta(seconds=run_time))
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return rst

    return wrapper


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    pass
