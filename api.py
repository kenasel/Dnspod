#coding=utf-8
import json
import requests
import fire
from setting import API,LOGIN_TOKEN




def get_domain():
    """
    curl -X POST https://dnsapi.cn/Domain.List -d 'login_token=LOGIN_TOKEN&format=json'
    """
    data = {"login_token": LOGIN_TOKEN, "format": "json"}
    r = requests.post(url=API + 'Domain.list', data=data)
    res = json.loads(r.text)
    return res['domains']



def creat_domain(domain):
    """
    curl -X POST https://dnsapi.cn/Domain.Create -d 'login_token=LOGIN_TOKEN&domain=api2.com&format=json'
    """
    data = {"login_token": LOGIN_TOKEN, "domain":domain, "format": "json"}
    r = requests.post(url=API + 'Domain.Create', data=data)
    res = json.loads(r.text)
    return res['domain']




def delete_domain(domain_id):
    """
    curl -X POST https://dnsapi.cn/Domain.Remove -d 'login_token=LOGIN_TOKEN&format=json&domain_id=1992403'
    """
    data = {"login_token": LOGIN_TOKEN, "format": "json", "domain_id":domain_id}
    r = requests.post(url=API + 'Domain.Remove', data=data)
    res = json.loads(r.text)
    return res['status']



def get_all_records(domain_id):
    """
    curl -X POST https://dnsapi.cn/Record.List -d 'login_token=LOGIN_TOKEN&format=json&domain_id=2317346'
    """
    data = {"login_token": LOGIN_TOKEN, "domain": domain_id, "format": "json"}
    r = requests.post(url=API + 'record.list', data=data)
    res = json.loads(r.text)
    return res['records']





def add_domain_record(domain_id, sub_domain, type ,record_line, ip, status, ttl=600):
    '''
    curl -X POST https://dnsapi.cn/Record.Create -d 'login_token=LOGIN_TOKEN&format=json&domain_id=2317346&sub_domain=@&record_type=A&record_line_id=10%3D3&value=1.1.1.1'
    '''
    data = {
        "login_token": LOGIN_TOKEN,
        "domain_id": domain_id,
        "sub_domain": sub_domain,
        "record_type": type,
        'record_line': record_line,
        "value": ip,
        'status': status,
        'ttl': ttl,
        "format": "json"
    }

    r = requests.post(url=API + 'Record.Create', data=data)
    res = json.loads(r.text)
    return res


def remove_record(domain_id, record_id):
    '''
    curl -X POST https://dnsapi.cn/Record.Remove -d 'login_token=LOGIN_TOKEN&format=json&domain_id=2317346&record_id=16894439'
    '''
    data = {
        "login_token": LOGIN_TOKEN,
        "domain_id": domain_id,
        'record_id': record_id,
        "format": "json"
    }

    r = requests.post(url=API + 'Record.Remove', data=data)
    res = json.loads(r.text)
    return res["status"]





def modify_record(record_id, record_line, type, ip, status, domain_id, sub_domain, ttl=600):
    """
    curl -X POST https://dnsapi.cn/Record.Modify -d 'login_token=LOGIN_TOKEN&format=json&domain_id=2317346&record_id=16894439&sub_domain=www&value=3.2.2.2&record_type=A&record_line_id=10%3D3'
    """
    data = {
        "login_token": LOGIN_TOKEN,
        "value": ip,
        "record_id": record_id,
        'record_line': record_line,
        "record_type": type,
        'status': status,
        "domain_id": domain_id,
        "sub_domain": sub_domain,
        "ttl": ttl,
        "format": "json"
    }
    r = requests.post(url=API + 'Record.Modify', data=data)
    res = json.loads(r.text)
    return res["status"]



def modify_record_status(domain_id, record_id, status):
    """
    curl -X POST https://dnsapi.cn/Record.Status -d 'login_token=LOGIN_TOKEN&format=json&domain_id=2317346&record_id=16894439&status=disable'
    """
    data = {
        "login_token": LOGIN_TOKEN,
        "domain_id": domain_id,
        'record_id': record_id,
        'status': status,
        "format": "json"
    }

    r = requests.post(url=API + 'Record.Status', data=data)
    res = json.loads(r.text)
    return res["status"]


if __name__ == "__main__":
    fire.Fire()
