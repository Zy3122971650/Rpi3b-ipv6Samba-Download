import download.downloadManage
import webapi.webApi
import subprocess
import time
import threading
import sys

class myThread(threading.Thread):
    def __init__(self,fn):
        threading.Thread.__init__(self)
        self.fn = fn
    def run(self):
        self.fn()

def redis():
    subprocess.Popen('redis-server --port 6380',shell=True)
    subprocess.Popen('redis-server --port 6381',shell=True)
    subprocess.Popen('redis-server',shell=True)
    subprocess.Popen('aria2c --conf-path={}/download/aria2/aria2.conf '.format(sys.path[0]),shell=True)
def main():
    myThread(redis).start()
    time.sleep(2)
    myThread(download.downloadManage.main).start()
    myThread(webapi.webApi.main).start()
    pass

if __name__ =='__main__':
    main()