# utf-8
import base64
import time
import urllib
from base64 import encode
from urllib.request import urlopen

from selenium import webdriver


def main():
    initUrls = []
    initUrls.append(
        'http://127.0.0.1:5000/1001233?userId=1001&channelNo=WFQD1001&tel=13518833380&userName=张女士&sex=0'
        '&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾')
    initUrls.append(
        'http://127.0.0.1:5000/1001234?userId=1002&channelNo=WFQD1001&tel=13646585588&userName=陈先生&sex=1'
        '&desc=倾向于三房两厅南北通透户型&projectId=1002&projectName=清水湾')
    initUrls.append(
        'http://127.0.0.1:5000/1001235?userId=1003&channelNo=WFQD1001&tel=13788888888&userName=王先生&sex=1'
        '&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城')
    initUrls.append(
        'http://127.0.0.1:5000/1001236?userId=1004&channelNo=WFQD1001&tel=13888888888&userName=黄先生&sex=1'
        '&desc=倾向于三房两厅南北通透户型&projectId=1002&projectName=清水湾')
    initUrls.append(
        'http://127.0.0.1:5000/1001237?userId=1005&channelNo=WFQD1001&tel=13988888888&userName=林先生&sex=1'
        '&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾')

    urls = []
    urls.append(
        'http://127.0.0.1:5000/1001238?userId=1006&channelNo=WFQD1001&tel=13699999999&userName=苏先生&sex=1'
        '&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城')
    urls.append(
        'http://127.0.0.1:5000/1001239?userId=1007&channelNo=WFQD1001&tel=15992428649&userName=罗先生&sex=1'
        '&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾')
    urls.append(
        'http://127.0.0.1:5000/1001240?userId=1008&channelNo=WFQD1001&tel=13518833380&userName=方先生&sex=1'
        '&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城')
    urls.append(
        'http://127.0.0.1:5000/1001243?userId=1009&channelNo=WFQD1001&tel=13485201258&userName=尉先生&sex=1'
        '&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾')
    urls.append(
        'http://127.0.0.1:5000/1001244?userId=1010&channelNo=WFQD1001&tel=13976536485&userName=黄女士&sex=0'
        '&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城')
    urls.append(
        'http://127.0.0.1:5000/1001245?userId=1011&channelNo=WFQD1001&tel=18876733310&userName=陈女士&sex=0'
        '&desc=倾向于三房两厅南北通透户型&projectId=1002&projectName=清水湾')
    urls.append(
        'http://127.0.0.1:5000/1001246?userId=1012&channelNo=WFQD1001&tel=13485201258&userName=罗女士&sex=0'
        '&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾')
    urls.append(
        'http://127.0.0.1:5000/1001247?userId=1013&channelNo=WFQD1001&tel=18289552238&userName=苏女士&sex=0'
        '&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城')
    urls.append(
        'http://127.0.0.1:5000/1001248?userId=1014&channelNo=WFQD1001&tel=15008925299&userName=王女士&sex=0'
        '&desc=倾向于三房两厅南北通透户型&projectId=1002&projectName=清水湾')
    urls.append(
        'http://127.0.0.1:5000/1001249?userId=1015&channelNo=WFQD1001&tel=13976536485&userName=钱女士&sex=0'
        '&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城')
    urls.append(
        'http://127.0.0.1:5000/1001250?userId=1016&channelNo=WFQD1001&tel=13800138000&userName=林女士&sex=0'
        '&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾')

    for url in initUrls:
        url = urllib.parse.quote(url, safe='/:?=.&')
        urlopen(url)

    time.sleep(40)
    for url in urls:
        url = urllib.parse.quote(url, safe='/:?=.&')
        urlopen(url)


if __name__ == '__main__':
    main()
