import redis
import json

def main():
    do = redis.Redis(host='localhost', port=6379,
                          db=0, decode_responses=True)
    wait = redis.Redis(host='localhost', port=6380,
                       db=0, decode_responses=True)
    cplct = redis.Redis(host='localhost', port=6381,
                        db=0, decode_responses=True)
    wait_data={
        'downloader':"aria2",
        'args':"http://app.mi.com/download/108048?id=com.tencent.tmgp.sgame&ref=search&nonce=-5583461006517876312%3A26646702&appClientId=2882303761517485445&appSignature=rn49x1c4IzNw667AVBZrp94Cet_Bb9Jyh9eQo5MF8MM"
    }
    while 1:
        flg = input("\
            清空3个数据库->1\n\
            打印3个数据库的keys->2\n\
            添加下载数据->3\n\
        ")
        if flg == '1':
            do.flushall()
            wait.flushall()
            cplct.flushall()
        elif flg =='2':
            print('do:',do.keys())
            print('wait:',wait.keys())
            print('finish:',cplct.keys())
        elif flg == '3':
            wait.set('0',json.dumps(wait_data))

main()