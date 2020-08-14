import os
import json
from QcloudApi.qcloudapi import QcloudApi
def get_ipv6():
    r = os.popen("ip addr")
    text = r.readlines()
    r.close()
    for txt in text:
        if ('inet6' in txt) and ('scope global' in txt):
            reslt = txt[10:][:-36]
            reslt = reslt[:reslt.find('/')]
            return reslt
    return None

def get_domain_id(ip):
    module = 'cns'

    # 对应接口的接口名，请参考wiki文档上对应接口的接口名
    action = 'RecordList'

    # 云API的公共参数
    config = {
        'secretId': 'XXXX',
        'secretKey': "XXX",
        'method': 'GET',
        'SignatureMethod': 'HmacSHA1',
        # 只有cvm需要填写version，其他产品不需要

    }

    # 接口参数，根据实际情况填写，支持json
    # 例如数组可以 "ArrayExample": ["1","2","3"]
    # 例如字典可以 "DictExample": {"key1": "value1", "key2": "values2"}
    action_params = {
        'domain': 'wdbefore.com',
    }

    try:
        service = QcloudApi(module, config)

        # 请求前可以通过下面几个方法重新设置请求的secretId/secretKey/Region/method/SignatureMethod参数
        # 重新设置请求的Region
        # service.setRegion('ap-shanghai')

        # 打印生成的请求URL，不发起请求
        print(service.generateUrl(action, action_params))
    # 调用接口，发起请求，并打印返回结果
        data = service.call(action, action_params)
    except Exception as e:
        import traceback
        print('traceback.format_exc():\n%s' % traceback.format_exc())
    data = json.loads(data)

    # 处理json 读记录ID Type Value

    records = data['data']['records']

    print(json.dumps(records, sort_keys=True, indent=4))
    for record in records:
        id_lst = []
        if record['type'] == 'AAAA' and record['name'] == 'home':
            action = 'RecordModify'
            # 例如字典可以 "DictExample": {"key1": "value1", "key2": "values2"}
            action_params = {
                'domain': 'wdbefore.com',
                'subDomain': 'home',
                'recordId': record['id'],
                'recordType': 'AAAA',
                'recordLine': '默认',
                'value': ip

            }

            try:
                service = QcloudApi(module, config)

                # 请求前可以通过下面几个方法重新设置请求的secretId/secretKey/Region/method/SignatureMethod参数
                # 重新设置请求的Region
                # service.setRegion('ap-shanghai')

                # 打印生成的请求URL，不发起请求
                print(service.generateUrl(action, action_params))
                # 调用接口，发起请求，并打印返回结果
                data = service.call(action, action_params)
            except Exception as e:
                print('traceback.format_exc():\n%s' %
                      traceback.format_exc())

ip = get_ipv6()
if ip != None:
    get_domain_id(ip)