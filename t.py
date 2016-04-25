import subprocess

# cmd = ["ls", "-F"]
# p = subprocess.Popen(args=cmd, shell=True)
# a = p.wait()
# subprocess.call(["ls", "-ll"])
p1 = subprocess.Popen(
    "adb shell am start -W -a \
    android.intent.action.SEND_MULTIPLE \
    -d file:///mnt/sdcard/Download/nexusx_1920x1080.png \
    -c android.intent.category.DEFAULT \
    com.alensw.PicFolder/com.alensw.transfer.TransferActivity",
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print p1.poll()
p1.wait()
stop_cmd = ['adb', 'shell', 'am', 'force-stop', 'com.alensw.PicFolder']
subprocess.Popen(stop_cmd)
print p1.poll()
p2 = subprocess.Popen(
    "adb shell am start -W -a \
    android.intent.action.SEND \
    -d file:///mnt/sdcard/Download/nexusx_1920x1080.png \
    -c android.intent.category.DEFAULT \
    com.alensw.PicFolder/com.alensw.transfer.TransferActivity",
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

(stdoutput, erroutput) = p2.communicate()
print stdoutput
