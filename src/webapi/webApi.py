from flask import Flask
from flask import request
from flask import jsonify
import redisdb.db as db

r = db.redisdb()

KEY = 'fakenews!'
app = Flask(__name__)


@app.route('/')
def index():
    return("There is nothing")


def get_args(args_dict) -> str:  # 参数拼接
    keys = args_dict.keys()
    arg = ''
    for key in keys:
        if key not in ['key','downloader']:
            arg += (' '+args_dict[key])
    return arg.strip()


@app.route('/download', methods=['POST'])
def download_any():

    if request.method == 'GET':
        # fake news
        return "OK"

    else:

        if request.form['key'] != KEY:
            # fake news
            return 'OK'

        elif request.form['downloader'] == 'you-get' or request.form['downloader'] == 'aria2':
            args = get_args(request.form)
            data = {} #args for you-get looks like '-xxx http://xxxxxxxx',and it for aria2 is a str, which translate from json object
            data['downloader'] = request.form['downloader']
            data['args'] = args
            r.w_set(data)
            return jsonify(date='Download join Wait Queue')

        else:
            return 'OK'


@app.route('/download/info', methods=['GET'])
def updata_download_info():
    json = r.d_get_all()
    return json

def main():
    import logging
    #log = logging.getLogger('werkzeug')
    #log.setLevel(logging.ERROR)
    app.run(port=8002,
        debug=False,
        host='::'
    )
    
if __name__ == "__main__":
    app.run(
        host='::',
        port=8002,
    )
