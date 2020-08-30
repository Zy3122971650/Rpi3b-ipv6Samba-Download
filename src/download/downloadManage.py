import json
import sys
sys.path.append('/home/zy/Rpi3BAndSamb')

import time
from concurrent.futures.thread import ThreadPoolExecutor

import src.download as download
import src.redisdb.db as db


MAXDOINGTASKS = 3

pool = ThreadPoolExecutor(MAXDOINGTASKS)


def download_you_get(args):
    download.you_get_download(args)


def download_aria2(args):
    download.aria2_download(args)

def test_main():
    while True:
        print(1)
def main():
    r = db.redisdb()
    while 1:
        doing_tasks = len(r.do.keys())
        wait_tasks = len(r.wait.keys())
        print (doing_tasks)
        if doing_tasks == MAXDOINGTASKS:
            print('跳过了')
            continue
        
        else:
            diff = MAXDOINGTASKS - doing_tasks
            tasks = r.wait.keys()[:diff]
            print(tasks)
            for task in tasks:
                data = json.loads(r.wait.get(task))
                method = data['downloader']
                if method == 'you-get':
                    pool.submit(download_you_get(data['args']))
                
                elif method == 'aria2':
                    pool.submit(download_aria2(data['args']))
                r.wait.delete(task)
        time.sleep(2)

if __name__ == "__main__":
    main()