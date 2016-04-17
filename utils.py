#!/usr/bin/env python
# -*- coding: utf-8 -*
import subprocess


def popen_wait(cmd):
    r = subprocess.Popen(cmd)
    r.wait()


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
