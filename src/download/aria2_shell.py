import sys
sys.path.append('/home/zy/Rpi3BAndSamb')
import requests
import json
import src.redisdb.db as db
r = db.redisdb()

# TODO：复用代码片段优化


class Aria2Api(object):
    def __init__(self):
        super().__init__()
        self.data = {
            'jsonrpc': '2.0',
            'id': '2333',
        }
        self.url = 'http://localhost:6800/jsonrpc'

    def _send_mssg(self, data: dict) -> dict:
        data_json = json.dumps(data)
        r = requests.post(self.url,data_json)
        dic_data = json.loads(r.text)
        return dic_data

    def _add_method(self, method: str):
        temp_dic = self.data.copy()
        temp_dic['method'] = method
        return temp_dic

    def _add_params(self, data: dict, params) -> dict:
        data['params'] = params
        return data

    def addUri(self, url) -> str:
        data = self._add_method('aria2.addUri')
        params = [[url]]
        data = self._add_params(data,params)
        gid = self._send_mssg(data)['result']
        return gid

    def tellStatus(self, gid):
        data = self._add_method('aria2.tellStatus')
        params = [gid]
        data = self._add_params(data, params)
        status = self._send_mssg(data)
        return status

    def tellSpeedStatus(self, gid) -> tuple:
        result = self.tellStatus(gid)['result']
        total_size = result['totalLength']
        size = result['completedLength']
        return (size, total_size)

    def tellFileName(self, gid) -> str:
        data = self._add_method('aria2.getFiles')
        params = [gid]
        data = self._add_params(data, params)
        file_path = self._send_mssg(data)['result'][0]['path']
        file_name = file_path.split('/')[-1]
        return file_name

    def tellActiveStatus(self, gid):
        result = self.tellStatus(gid)['result']
        status = result['status']
        return status

    def get_download_info(self, gid):
        size, total_size = self.tellSpeedStatus(gid)
        file_name = self.tellFileName(gid)
        return (file_name, size, total_size)

    def remove(self, gid):
        data = self._add_method('aria2.remove')
        params = [gid]
        data = self._add_params(data, params)
        self._send_mssg(data)


def updata_download_info(data: dict):
    r.d_set(data)


def remove_download_info(title: str):
    r.d2c_one(title)


def main(args):
    a = Aria2Api()
    gid = a.addUri(args)
    data = {}
    data['origin'] = args
    while 1:
        title, size, total_size = a.get_download_info(gid)
        data['title'] = title
        data['size'] = size
        data['total_size'] = total_size
        updata_download_info(data)
        if a.tellActiveStatus(gid) not in ['active','waiting']:
            remove_download_info(title)
            a.remove(gid)
            break

if __name__ == "__main__":
    main('http://download.kugou.com/download/kugou_pc')