import sys
sys.path.append('/home/zy/Rpi3BAndSamb')

import src.download.downloadManage
import src.webapi.webApi
import subprocess
from concurrent.futures.process import ProcessPoolExecutor

def redis():
    subprocess.Popen('redis-server --port 6380',shell=True)
    subprocess.Popen('redis-server --port 6381',shell=True)
    subprocess.Popen('redis-server',shell=True)
    subprocess.Popen('aria2c --conf-path=/home/zy/Rpi3BAndSamb/src/download/aria2/aria2.conf ',shell=True)
def main():
    process_pool = ProcessPoolExecutor()
    process_pool.submit(redis)
    process_pool.submit(src.download.downloadManage.main())
    process_pool.submit(src.webapi.webApi.main)
    pass

if __name__ =='__main__':
    main()