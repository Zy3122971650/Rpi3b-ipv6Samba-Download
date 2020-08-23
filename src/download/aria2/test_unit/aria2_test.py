import json
import requests

data = {
    'jsonrpc': '2.0',
    'id': 'qwe',
    'method': 'aria2.addUri',
    'params': [["http://download.kugou.com/download/kugou_pc"]]
}
data_s = json.dumps(data)
r = requests.post('http://localhost:6800/jsonrpc', data_s)
print(r.text)

