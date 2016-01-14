"""
/*
 * Android framework fuzzer
 * Author: wcx
 * 对以文件为输入的Android APP 进行Fuzzing，收集错误信息，进行分类
 */

"""
import os
import subprocess


def popen_wait(cmd, message=None):
    '''
    开始一个子进程
    '''
    p = subprocess.Popen(cmd)
    ret_val = p.wait()
    if message:
        print(message)
    return ret_val


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


def main():
    print("Start Pushing")
    files = push_files()
    print (files)
    print("Done pushing")


if __name__ == '__main__':
    main()
