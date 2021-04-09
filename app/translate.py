# 开发者: 朱仁俊
# 开发时间: 2021/4/9  11:12

import json, random, hashlib, http.client

from flask import current_app
from flask_babel import _
# from app import app
from urllib import parse


def translate(q, fromLang, toLang):
    if 'APPID' not in current_app.config or not current_app.config['APPID']:
        return _('Error:the translation service is not configured.')
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error:the translation service is not configured.')
    appid = current_app.config['APPID']
    secretKey = current_app.config['MS_TRANSLATOR_KEY']

    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    # 形式: http://api.fanyi.baidu.com/api/trans/vip/translate?appid=20180824000198587&q=apple&from=en&to=zh&salt=60422&sign=92ec698844333d1e9f04b756d14ae95d
    try:
        # 客户端去访问百度翻译的服务器
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # 获取百度翻译服务器的回应 并将回应解码为字符串 通过json转化为字典 从而提取字典中翻译结果
        response = httpClient.getresponse()  # response是HTTPResponse对象
        r = response.read().decode('utf-8')
        d = json.loads(r)

        l = d['trans_result']
        l1 = l[0]['dst']

        return (l1)
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
