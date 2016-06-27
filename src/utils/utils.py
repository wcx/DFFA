#!/usr/bin/env python
# -*- coding: utf-8 -*
import subprocess
import time
from datetime import timedelta


def home_screen():
    return send_key_event('3')


def send_key_event(event_num):
    cmd = ['adb', 'shell', 'input', 'keyevent', event_num]
    popen_wait(cmd)


def print_symbol(string):
    print("---------------------------------------" + string +
          "---------------------------------------------------")


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


def popen_wait(cmd):
    p = subprocess.Popen(to_cmd_str(cmd), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    p.wait()
    return p


def timeout_cmd(cmd, timeout=60):
    """
    执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    :param cmd: 要执行的命令
    :param timeout: 最长等待时间，单位：秒
    :return:
    """
    cmd = to_cmd_str(cmd)
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        if p.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            p.terminate()
            raise TimeoutError(cmd, timeout)
        time.sleep(0.1)
    return p


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


if __name__ == "__main__":
    pass
