import subprocess
import os
import json
import redisdb.db as db
r = db.redisdb()

def download(path: str, args: str) -> list:  # [title,current_size,total_size]
    t = subprocess.Popen(path+args,
                         stdout=subprocess.PIPE,
                         bufsize=1,
                         encoding='utf-8',
                         shell=True)
    data = {}
    data['origin'] = args
    while 1:
        try:
            txt = t.stdout.readline()
            if 'title' in txt:
                data['title'] = txt.split(':')[1]

            if '%' in txt:
                start = list(txt).index('(')
                end = list(txt).index(')')
                str1 = txt[start+1:end-2]
                data['total_size'] = str1.split('/')[0]
                data['size'] = str1.split('/')[1]
                updata_download_info(data)

            if txt == 'DownLoad-Done':
                remove_download_info(data['origin'])
                break

            assert 'Wrong' not in txt
        except:
            print('Something Wrong')
            remove_download_info(data['origin'])
            break


def updata_download_info(data: dict):
    r.d_set(data)

def remove_download_info(args:str):
    r.d2c_one(args)

def scrip_main(args: str):
    # path = sys.path[0] +'/src/download/you_get/you-get'  #入口得是从Rpi3BAndSamb开始
    path = sys.path[0] + '/download/you_get/you-get'#main.py为入口，从Rpi....、/src开始
    with open(path + '/download/you_get_download_save_file_path.txt','r+') as f:
        put_dir_path = f.readline()[:-2]
    args = ' '+args+' -o '+put_dir_path #制作参数
    download(path, args)
    pass


def updata_you_get():
    pass


def main(args):
    scrip_main(args)



if __name__ == "__main__":
    while 1:
        mean = input('Do you want to check && updata you-get [y/n]')
        if mean == 'y':
            updata_you_get()
            print('Done')
            break
        elif mean == 'n':
            break
        else:
            continue
"""

if __name__ == "__main__":
    args = ''
    for arg in sys.argv[1:]:
        args += (' '+arg)
    main(args)
"""