import src.redisdb.db as db
from concurrent.futures.thread import ThreadPoolExecutor
import json

MAXDOINGTASKS = 3

pool = ThreadPoolExecutor()

def download_you_get():
    pass

def download_aria2():
    pass

def main():
    r = db.redisdb()
    while 1:
        doing_tasks = len(r.do.keys())
        wait_tasks = len(r.wait.keys())
        if doing_tasks == MAXDOINGTASKS:
            continue
        else:
            diff = MAXDOINGTASKS - doing_tasks
            tasks = r.wait.keys()[:diff]
            for task in tasks:
                data = json.loads(r.wait.get(task))
                method = data['downloader']
                if method == 'you-get':
                    pool.submit(download_you_get())
                elif method == 'aria2':
                    pool.submit(download_aria2())
