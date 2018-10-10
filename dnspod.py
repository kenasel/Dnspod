import json
import requests
import fire
from setting import API,LOGIN_TOKEN

class Dnspod(object):
    def __init__(self, LOGIN_TOKEN, API):
        self.dnspodapi = API
        self.dnspod_login_token = LOGIN_TOKEN

    def get_record(self, domain, sub_domain):
        data = {
            "login_token": self.dnspod_login_token,
            "domain": domain,
            "sub_domain": sub_domain,
            "format": 'json'
        }

        try:
            request = requests.post(url=self.dnspodapi + 'record.list', data=data)
            res = json.loads(request.text)
            if 'status' in res and res['status']['code'] == '1':
                return res['records']
            else:
                return False
        except  requests.exceptions.RequestException as e:
            print(e)
            return False


    def get_info_record(self, domain, sub_domain):
        res = self.get_records(domain, sub_domain)
        if res:
            for i in res:
                print(i['id'], i['name'], i['value'], i["status"], i['enabled'], i['line'], 'line_id:', i['line_id'], 'remark', i['remark'])


    def get_record_by_ip(self, ip, domain, sub_domain):
        res = self.get_records(domain, sub_domain)
        if res:
            record_id = None
            record_line_id = None
            for i in res:
                if i['value'] == ip:
                    record_id =  i['id']
                    record_line_id = i['line_id']
            return record_id,record_line_id
        else:
            print('Get DNSPod records failed!')
            return None,None

    def get_record_status_by_ip(self, ip, domain, sub_domain):
        res = self.get_records(domain, sub_domain)
        if res:
            record_status = None
            for i in res:
                if i['value'] == ip:
                    record_status =  int(i['enabled'])
            return record_status
        else:
            print('Get DNSPod records status failed!')
            return False

    def add_record(self, ip, record_line, status, domain, sub_domain):
        record_id, record_line_id = self.get_record_by_ip(ip, domain, sub_domain)
        if record_id !=None and record_line_id != None:
            print('%s %s.%s exists'%(ip,sub_domain,domain))
            return False
        else:
            data = {
                "login_token": self.dnspod_login_token,
                "domain": domain,
                "sub_domain": sub_domain,
                "record_type": 'A',
                'record_line': record_line,
                "value": ip,
                "status": status,
                "ttl": 600,
                "format": 'json'
            }
            try:
                request = requests.post(url=self.dnspodapi + 'Record.Create', data=data)
                res = json.loads(request.text)
                return int(res['status']['code'])
            except  requests.exceptions.RequestException as e:
                print(e)
                return False

    def del_record(self, ip, domain, sub_domain):
        record_id,record_line_id = self.get_record_by_ip(ip, domain, sub_domain)
        if record_id:
            data = {
                "login_token": self.dnspod_login_token,
                "domain": domain,
                "record_id": record_id,
                "format": "json"
            }
            try:
                request = requests.post(url=self.dnspodapi + 'Record.Remove', data=data)
                res = json.loads(request.text)
                if 'status' in res and res['status']['code'] == '1':
                    return True
                else:
                    return False
            except  requests.exceptions.RequestException as e:
                print(e)
                return False
        else:
            print('Get %s %s.%s record failed!'%(ip,sub_domain, domain))
            return False

    def modify_record(self, ip,record_id,record_line_id,status,domain, sub_domain):
        data = {
            "login_token": self.dnspod_login_token,
            "value": ip,
            "record_id": record_id,
            "record_line_id": record_line_id,
            "record_type": 'A',
            "status": status,
            "domain": domain,
            "sub_domain": sub_domain,
            "format": 'json'
        }
        try:
            request = requests.post(url=self.dnspodapi + 'Record.Modify', data=data)
            res = json.loads(request.text)
            if 'status' in res and res['status']['code'] == '1':
                return True
            else:
                return False
        except  requests.exceptions.RequestException as e:
            print(e)
            return False

    def modify_record_status(self, domain, sub_domain, ip, status):
        record_id,record_line_id  = self.get_record_by_ip(ip, domain, sub_domain)
        if record_id !=None and record_line_id != None:
            return self.modify_record(ip, record_id, record_line_id, status, domain, sub_domain)
        else:
            print('Get record info failed %s'%ip)
            return False


    def add_record_remark(self,ip, remark, domain, sub_domain):
        record_id,record_line_id = self.get_record_by_ip(ip, domain, sub_domain)
        if record_id:
            data = {
                "login_token": self.dnspod_login_token,
                "domain": domain,
                "record_id": record_id,
                "remark": remark,
                "format": "json"
            }
            try:
                request = requests.post(url=self.dnspodapi + 'Record.Remark', data=data)
                res = json.loads(request.text)
                if 'status' in res and res['status']['code'] == '1':
                    return True
                else:
                    return False
            except  requests.exceptions.RequestException as e:
                print(e)
                return False
        else:
            print('Get %s record failed!'%ip)
            return False

if __name__ == '__main__':
    fire.Fire(Dnspod('22715,bf07e776bae1b3238c654675c6a1c329'))

