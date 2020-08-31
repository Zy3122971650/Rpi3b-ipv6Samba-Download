import json

import time
import download as download
import redisdb.db as db
import threading

class aria2Thread(threading.Thread):
    def __init__(self,args):
        threading.Thread.__init__(self)
        self.args = args
    def run(self):
        download_aria2(self.args)

class youGetThread(threading.Thread):
    def __init__(self,args):
        threading.Thread.__init__(self)
        self.args = args
    def run(self):
        download_you_get(self.args)


MAXDOINGTASKS = 3

def download_you_get(args):
    download.you_get_download(args)


def download_aria2(args):
    download.aria2_download(args)

def test_main():
    while True:
        print(1)
def test1(obj):
    print(1)
def main():
    r = db.redisdb()
    while 1:
        #TODO:好像出现了往do里面重复添加的问题
        doing_tasks = len(r.do.keys())
        wait_tasks = len(r.wait.keys())
        #print (doing_tasks)
        if doing_tasks == MAXDOINGTASKS:
            print('跳过了')
            continue
        
        else:
            diff = MAXDOINGTASKS - doing_tasks
            tasks = r.wait.keys()[:diff]
            #print(tasks)
            for task in tasks:
                data = json.loads(r.wait.get(task))
                r.wait.delete(task)
                method = data['downloader']
                if method == 'you-get':
                    youGetThread(data['args']).start()
                elif method == 'aria2':
                    #time1 = time.time()
                    #pool.submit(download_aria2(data['args'])).add_done_callback(test1) #####这是一个堵塞的方法，要改成非堵塞的，其他的异常应该也是使用了这种方法导致的
                    aria2Thread(data['args']).start()
                    #print(time.time()-time1)
        time.sleep(0.5)

if __name__ == "__main__":
    main()