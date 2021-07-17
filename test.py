import subprocess

cmd = "echo 'shit' | gpg --decrypt"
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output = ps.communicate()[0].decode("utf-8")
print(output)