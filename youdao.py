#coding=utf-8
import requests
import random
import time
import socket
import json
import os
import codecs



header={
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.3',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Referer': 'http://note.youdao.com/signIn/index.html?&callback=https%3A%2F%2Fnote.youdao.com%2Fweb%2F%23%2Ffile%2Frecent%2Fnote%2FWEBc56d7c0f89ad3839112a04b2f884e9e3%2F',
	'Accept-Encoding': 'gzip, deflate, sdch, br',
	'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Content-Type':'text/html; charset=utf-8',
    'Cookie':'YOUDAO_EAD_UUID=e862db00-d069-4ebf-bbf7-3570d3b56adf; OUTFOX_SEARCH_USER_ID_NCOO=817327912.119402; __yadk_uid=er3uHnrmk7hcUvdX8wTcfcLSNTEw6ZmB; _ntes_nnid=648a1769db6036e5011db0dc4b5c5f12,1472441696340; P_INFO=zf9876@163.com|1473723647|2|mail163|11&18|bej&1473598442&note_client#bej&null#10#0#0|131523&0|mail163&note_client|zf9876@163.com; Hm_lvt_8875c662941dbf07e39c556c8d97615f=1472959142,1473141521,1473232855,1474177796; crtg_rta=; OUTFOX_SEARCH_USER_ID=-1608805638@119.161.147.101; JSESSIONID=aaaWZL6I_Vk4Y_Ui8gdDv; ___rl__test__cookies=1474959213650; Hm_lvt_30b679eb2c90c60ff8679ce4ca562fcc=1474514362,1474959214; Hm_lpvt_30b679eb2c90c60ff8679ce4ca562fcc=1474959214; YNOTE_CSTK=2u-EQX1Y; Hm_lvt_4566b2fb63e326de8f2b8ceb1ec367f2=1472382360,1474514364,1474959215; Hm_lpvt_4566b2fb63e326de8f2b8ceb1ec367f2=1474960124; _ga=GA1.2.1604179404.1472382360'
}


    # return html_text
    # https://note.youdao.com/yws/api/personal/sync?method=download&cstk=2u-EQX1Y&keyfrom=web
    # https://note.youdao.com/login/acc/login?username=zf9876%40163.com&password=fa32d152ba6c4f0bfac67a245159527e&app=web&product=YNOTE&tp=urstoken&cf=6&fr=1&systemName=&deviceType=&ru=http%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&er=http%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&systemName=mac&deviceType=MacPC&timestamp=1474960117512
    # http://note.youdao.com/signIn//loginCallback.html?product=YNOTE&tp=urstoken&app=web&s=true
payload={
    'version':'-1',
    'convert':'true',
    'editorType':'0',
    'cstk':'2u-EQX1Y'
}
resp = requests.get("https://note.youdao.com/login/acc/login?username=zf9876%40163.com&password=fa32d152ba6c4f0bfac67a245159527e&app=web&product=YNOTE&tp=urstoken&cf=6&fr=1&systemName=&deviceType=&ru=http%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&er=http%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&systemName=mac&deviceType=MacPC&timestamp=1474960117512",headers = header, allow_redirects=False)
resp.encoding='utf8'
print(resp.text)

_cookies = resp.cookies
print _cookies
resp = requests.get("http://note.youdao.com/yws/mapi/user?method=get&multilevelEnable=true&_=1474960097653", cookies=_cookies)
resp.encoding='utf-8'
print(resp.text)
resp = requests.get("https://note.youdao.com/yws/api/personal/file/FD50ABAA92B9436F9E64AE7C742070C2?cstk=2u-EQX1Y&dir=false&f=true&isReverse=false&keyfrom=web&len=30&method=listPageByParentId&sort=1", cookies=_cookies)
resp.encoding='utf-8'
print(resp.text)

decodejson = json.loads(resp.text)
print type(decodejson)

file_object = codecs.open('/work/tmp/youdaonote.html', 'w', 'utf-8')
try:
    file_object.writelines('<!DOCTYPE html><html><head><title>note</title><meta charset="utf-8"></head><body>')
    for i in range(0, len(decodejson['entries'])):
        _fileId =  decodejson['entries'][i]['fileEntry']['id']
        payload['fileId'] = _fileId
        print payload
        resp = requests.get("https://note.youdao.com/yws/api/personal/sync?method=download&cstk=2u-EQX1Y&keyfrom=web", params=payload, cookies=_cookies)
        resp.encoding='utf-8'
        file_object.write(resp.text)
    file_object.writelines('</body></html>')
finally:
    file_object.close()
os.system('/work/tools/KindleGen_Mac_i386_v2_9/kindlegen /work/tmp/youdaonote.html -o youdaonote.mobi -locale zh')