import subprocess
# p=subprocess.Popen("dir", shell=True)
# p.wait()
p=subprocess.Popen("dir", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(stdoutput,erroutput) = p.communicate()
