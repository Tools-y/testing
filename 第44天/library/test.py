# test=__import__('analyseAA',fromlist=True)
# test.gets('192.168.52.133','root','C:/Users/THINK/.ssh/id_rsa')
import subprocess
import  time
import  datetime
import psutil
# cpuinfo=psutil.cpu_times()
# print(cpuinfo)
# cpu=psutil.cpu_percent(1,True)
# print(cpu)
# result=subprocess.Popen('cat  /etc/passwd',shell=True,stdout=subprocess.PIPE)
# print(result,type(result))
# print(result.stdout.readlines(),type(result.stdout))
# print(type(subprocess.Popen('cat  /etc/passwd',shell=True)))
dat = time.strftime('%Y%m%d%H%M%S', time.localtime())
print(dat,type(dat))
print(time.localtime())
print(time.time())
print(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
print(datetime.datetime.now())
