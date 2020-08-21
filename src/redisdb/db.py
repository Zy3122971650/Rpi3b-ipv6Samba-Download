import redis
import json


class redisdb(object):

    def __init__(self):
        super().__init__()
        # TODO:Use one redis server to maintain three list(wait list && doing list && finish list)
        # r->read w->wait
        self.do = redis.Redis(host='localhost', port=6379,
                              db=0, decode_responses=True)
        self.wait = redis.Redis(host='localhost', port=6380,
                                db=0, decode_responses=True)
        self.cplct = redis.Redis(host='localhost', port=6381,
                                 db=0, decode_responses=True)

    def redisset(self, data: dict, obj):
        """
        Pass in a dict,which should includ value of (tittle size total_size)
        """
        data_s = json.dumps(data)
        Id = self.check_is_exist(data['title'])
        if Id == None:
            Id = self.find_suit_id(obj)
        obj.set(Id, data_s)

    def d_set(self, data: dict):
        self.redisset(data, self.do)

    def w_set(self, data: dict):
        self.redisset(data, self.wait)
    
    def c_set(self, data: dict):
        self.redisset(data, self.cplct)

    def find_suit_id(self, obj):
        keys = obj.keys()
        for i in range(100):
            if str(i) not in keys:
                return str(i)

    def redisget_all(self, obj):
        keys = obj.keys()
        values = obj.mget(keys)
        dic = {}
        for i in range(len(values)):
            dic[str(i)] = values[i]
        data = json.dumps(dic)
        return data

    def w_get_all(self):
        self.redisget_all(self.wait)

    def d_get_all(self):
        self.redisget_all(self.do)

    def c_get_all(self):
        self.redisget_all(self.cplct)

    def check_is_exist(self, title: str):
        for key in self.do.keys():
            data = json.loads(self.do.get(key), encoding='utf-8')
            if data['title'] == title:
                return key
        return None

    def check_full(self):
        if len(self.do.keys()) >= 10:
            return True
        return False

    def d2c(self, keys):
        for key in keys:
            value = self.wait.get(key)
            Id = self.find_suit_id(self.do)
            self.do.set(Id, value)
    
    def d2c_one(self,title):
        keys = self.do.keys()
        for key in keys:
            data = json.loads(self.do[key])
            if data['title'] == title:
                Id = self.find_suit_id(self.cplct)
                self.cplct.set(Id,self.do[key])

    def check_speed(self):
        pass

    def check_complect_err(self):
        pass

    def check_size(self):
        pass

    def auto_remove_download_info(self):
        pass

    def save(self):
        def save_date(self, name, ob):
            with open(name, 'w+') as f:
                for key in self.ob.keys():
                    f.write(key, self.ob.get(key))
        save_date('wait.db', self.wait)
        save_date('doing.db', self.do)

    def load(self):
        pass
