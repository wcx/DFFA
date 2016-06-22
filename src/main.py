"""
/*
 * Android framework fuzzer
 * Author: wcx
 * 对以文件为输入的Android APP 进行Fuzzing，收集错误信息，进行分类
 */

"""
import os
import subprocess
import json
import re
import pexpect
import glob
from install import PackageInstaller


class AndroidLogger:
    '''
    从Android device/emulator收集logs
    '''

    def __init__(self, log_dir='logs'):
        self.logs = {}
        log_cmd = 'adb -e logcat'
        self.logfile = log_dir + '/logfile'
        # self.add_log_dir(log_dir)
        self.child = pexpect.spawn(log_cmd)
        try:
            self.child.read_nonblocking(timeout=0)
        except pexpect.TIMEOUT:
            pass

    def add_log_dir(self, log_dir):  # Bug, 如果存在相同文件名呢？
        if log_dir[-1] != '/':
            log_dir += '/'
        if os.path.isdir(log_dir):
            self.log_dir = log_dir
            return log_dir
        else:
            os.makedirs(log_dir)
            return self.add_log_dir(log_dir)

    def __read(self):
        '''
        从ADB读取log
        '''
        try:
            self.child.expect('\r\r\n', timeout=5)
            log_output = self.child.before
        except pexpect.TIMEOUT:
            log_output = None
        return log_output

    def write_app_logs(self, program):
        '''
        向当前文件写入log
        '''
        # logs_dict = self.pop_program_logs(program)
        # self.logfile.write(json.dumps(logs_dict))
        # if check_segfault(logs_dict):
        #     self.logfile.write(program +'\n\n\n')
        #     self.logfile.write(unicode(logs_dict))
        #     self.logfile.close()
        return self.logfile

    def add_app(self, app):

        # if self.logfile:
        #     self.logfile.close()
        #     self.logfile = None
        self.logs[app] = {}
        # log_path = self.log_dir + '/' + app + '.log'
        # self.logfile = open(log_path, 'a+')
        return self.logs[app], self

    def get_logs(self):
        '''
        返回adb logs
        '''
        return self.logs

    def pop_program_logs(self, program):
        '''
        返回logs
        '''
        return self.logs.pop(program, {})

    def add_logs(self, app, file):
        '''
        向每一行添加log信息
        '''
        log_lines = self._get_logs(app, file)
        # self.check_segfault(log_lines, app, file)
        self.logs[app][file] = log_lines
        # file_log = {file: '\n'.join(log_lines)}
        if check_segfault(self.logs[app]):
            print "segf"
            self.logfile.write(file + '\t' + app + '\n')
            self.logfile.flush()
            self.logs[app][file] = ''
            # self.logfile.write(unicode(self.logs[app]))
        return self.logs[app][file]

    def _get_logs(self, app, file):
        '''
        持续从Android devices获取Log
        '''
        logs = ''
        while True:
            log_line = self.__read()
            if not log_line:
                break
            logs = '\n'.join([logs, log_line])
        return logs


def push_files(remote_path='/mnt/sdcard/Download', local_path='pdfs', adb='adb'):
    '''
    向android devices push files
    '''
    cmd = [adb, 'push', local_path, remote_path]
    popen_wait(cmd)
    files = os.listdir(local_path)
    remote_files = [remote_path + '/' + file for file in files]
    return remote_files


def stop_app(application, process=None):
    '''
    开始运行APP
    '''
    if process:
        process.kill()
    home_screen()  # Can't kill apps in foreground
    stop_cmd = ['adb', 'shell', 'am', 'force-stop', application]
    return popen_wait(stop_cmd)


def popen_wait(cmd, message=None):
    '''
    开始一个子进程
    '''
    p = subprocess.Popen(cmd)
    ret_val = p.wait()
    if message:
        print(message)
    return ret_val


def open_file(file, intent, mimetype):
    '''
    创造一个 打开文件的Popen object并且返回 Popen object
    '''
    data = 'file://' + file
    open_cmd = ['adb', 'shell', 'am', 'start', '-W',
                '-a', intent, '-d', data, '-t', mimetype]
    p = subprocess.Popen(open_cmd)
    return p


def open_files(files, intent='android.intent.action.VIEW', mimetype='application/pdf', log_dir='logs'):
    logger = AndroidLogger(log_dir)
    package_installer = PackageInstaller()
    applications = package_installer.install_applications()
    app_logfiles = []
    for application in applications:
        logger.add_app(application)
        stop_app(application)
        for file in files:
            p = open_file(file, intent, mimetype)
            logger.add_logs(application, file)
            stop_app(application, process=p)
        application = package_installer.uninstall(application)
    return app_logfiles


def home_screen():
    '''
    向Android Device发送HOME键动作事件
    '''
    return send_key_event('2')


def send_key_event(event_num):
    '''
    向Android Device发送任意键动作事件
    '''
    cmd = ['adb', 'shell', 'input', 'keyevent', event_num]
    return popen_wait(cmd)


def power_button():
    '''
    向Android Device发送POWER键动作事件
    '''
    return send_key_event('26')


def kill_app(app):
    '''
    终止APP进程
    '''
    stop_app(app)
    kill_cmd = ['adb', 'shell', 'am', 'kill', app]
    return popen_wait(kill_cmd)


def adb_cmd(cmd):
    '''
    ADB命令
    '''
    return ['adb'] + cmd


def adb_shell_cmd(cmd):
    '''
    Shell命令
    '''
    return adb_cmd(['shell']) + cmd


def cleanup(files):
    '''
    清除文件
    '''
    return popen_wait(adb_shell_cmd(['rm'] + files))


def check_segfault(log_dict):
    # regex = r'F/libc    \(  \d*\): Fatal signal \d{2,8} .*terminated by signal \(11\)'# r'Fatal signal 11(.|\n)*Process \d{2,8} terminated by signal'
    # regex = ur'F/libc    \(  \d*\): Fatal signal \d{2,8} .*terminated by signal \(11\)'
    # match = re.search(regex, log)
    # if match:
    #     return match.group()
    # else:
    #     return None
    segfault_caused = False
    files = log_dict.keys()
    for file in files:
        if 'Fatal signal 11' in log_dict[file]:
            print "Segfault caused by " + file
            segfault_caused = True
    return segfault_caused


def fuzz(log_dir='logs'):
    '''
    向Android device push files,安装APP并且开始FUZZING
    '''
    files = push_files()
    logs = open_files(files, log_dir=log_dir)
    return logs, files


# def examine_logs(log_dir):
# if log_dir[-1] != '/': # should make a decorator
#         log_dir += '/'
#     logs = glob.glob(log_dir + '*.log')
#     for log_file in logs:
#         log_file_fp = open(log_file)
#         log_file_contents = log_file_fp.read()
#         log_file_fp.close()
#         check_segfault(json.loads(log_file_contents))
# segfault_logs = check_segfault(log_file_contents)
# if segfault_logs:
# segfault_logs_fp = json.loads(open(logfile + '.segfault', 'w+'))
# segfault_logs_fp.write(segfault_logs)


def main():
    log_dir = 'logs'
    _, fuzz_files = fuzz(log_dir=log_dir)
    print "Done Fuzzing"
    # examine_logs(log_dir)
    print "Done logging"
    cleanup(fuzz_files)


if __name__ == '__main__':
    main()
