#!/usr/bin/env python
# -*- coding: utf-8 -*
import subprocess
import time


def home_screen():
    '''
    向Android Device发送HOME键动作事件
    '''
    return send_key_event('3')


def send_key_event(event_num):
    '''
    向Android Device发送任意键动作事件
    '''
    cmd = ['adb', 'shell', 'input', 'keyevent', event_num]
    popen_wait(cmd)


def print_symbol(str):
    print("---------------------------------------" + str +
          "---------------------------------------------------")


def to_cmd_str(cmd):
    return ' '.join(str(i) for i in cmd)


class TimeoutError(Exception):
    pass


def popen_wait(cmd):
    p1 = subprocess.Popen(to_cmd_str(cmd), shell=True)
    p1.wait()

def timeout_cmd(cmd, timeout=60):
    """执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    cmd - 要执行的命令
    timeout - 最长等待时间，单位：秒
    """
    cmd=to_cmd_str(cmd)
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


class logger(object):
    def info(self, info):
        print info


if __name__ == "__main__":
    print timeout_cmd(cmd='ping www.redicecn.com')
