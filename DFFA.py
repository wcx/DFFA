"""
/*
 * Android framework fuzzer
 * Author: wcx
 * 对以文件为输入的Android APP 进行Fuzzing，收集错误信息，进行分类
 */

"""
import os
from utils import *


def push_files():
    '''
    向android devices push files
    '''
    local_path = 'pdfs'
    remote_path = '/mnt/sdcard/FuzzDownload'
    cmd = ['adb', 'push', local_path, remote_path]
    popen_wait(cmd)
    files = os.listdir(local_path)
    remote_files = [remote_path + '/' + file for file in files]
    return remote_files


def open_file(files):
    intent = 'android.intent.action.VIEW'
    mimetype = 'application/pdf'
    for file in files:
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
    rm_cmd = ['adb', 'shell', 'rm'] + files
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

if __name__ == '__main__':
    main()
