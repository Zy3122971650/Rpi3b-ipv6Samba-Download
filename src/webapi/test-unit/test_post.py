import requests
import json
data = {
    'key':'fakenews!',
    'downloader':'aria2',
    'url':"http://download.kugou.com/download/kugou_pc"
}
r = requests.post('http://127.0.0.1:8002/download',data)
print(r)