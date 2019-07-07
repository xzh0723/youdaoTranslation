# -*- coding: utf-8 -*-
# @Time    : 2019/7/7 22:02
# @Author  : xuzhihai0723
# @Email   : 18829040039@163.com
# @File    : youdao.py
# @Software: PyCharm

import hashlib
import requests
import time
import execjs

def md5_encrypt(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

def get_salt(timestamp):
    js = """
    function get_salt(timestamp) {
        return (timestamp + parseInt(10 * Math.random(), 10))
    }
    """
    ctx = execjs.compile(js)
    salt = ctx.call('get_salt', timestamp)
    return salt

def run():
    api = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    keyword = input('你要翻译啥>> \n')

    headers = {
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-1867145421@10.108.160.17; JSESSIONID=aaa4aprbywi3fhv_DTmVw; OUTFOX_SEARCH_USER_ID_NCOO=1231020454.0353444; ___rl__test__cookies=1562508084293',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    }
    timestamp = int(time.time() * 1000)
    salt = get_salt(timestamp)
    data = {
        'i': keyword,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': str(salt),
        'sign': md5_encrypt("fanyideskweb" + keyword + str(salt) + "@6f#X3=cCuncYssPsuRUE"),
        'ts': str(timestamp),
        'bv': md5_encrypt(headers['User-Agent'][8:]),
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }

    res = requests.post(api, data=data, headers=headers)
    print(res.json())

if __name__ == '__main__':
    run()


