from flask import Flask
from flask import Request
from flask import jsonify
import src.redisdb.db as db

r = db.redisdb()

KEY = 'fake news!'
app = Flask(__name__)


@app.route('/')
def index():
    return("There is nothing")


def get_args(args_dict) -> str:  # 参数拼接
    keys = args_dict.keys()
    arg = ''
    for key in keys:
        arg += (' '+args_dict[key])
    return arg


@app.route('/download', methods=['POST', 'GET'])
def download_any():

    if Request.method == 'GET':
        # fake news
        return "OK"

    else:

        if Request.form['key'] != KEY:
            # fake news
            return 'OK'

        elif Request.form['downloader'] == 'you-get' or Request.form['downloader'] == 'aria2':
            args = get_args(Request.form)
            data = {}
            data['downloader'] = Request.form['downloader']
            data['args'] = args
            r.redisset(data)
            return jsonify(date='Download join Wait Queue')

        else:
            return 'OK'


@app.route('/download/info', method='GET')
def updata_download_info():
    json = r.redisget_all()
    return json


if __name__ == "__main__":
    app.run(
        port=8002
    )
    pass
