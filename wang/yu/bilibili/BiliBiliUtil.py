import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import os
from wang.yu.common.PyXmlParser import PyXmlParser

py_xml_parser = PyXmlParser(os.path.dirname(os.path.dirname(__file__)) + '/common/properties/properties.xml')
print(os.path.dirname(os.path.dirname(__file__)) + '/common/properties/properties.xml')
xml = py_xml_parser.do_parse()
page_list_prefix = xml['websites']['bilibili']['page-list-prefix']
av_id = input('输入av号:')
# page_list_url = getlist_prefix.replace('AID_PLACEHOLDER', av)
# TODO remove once coded
page_list_url = page_list_prefix.replace('AID_PLACEHOLDER', '2528486')
print(page_list_url)
page_list = requests.get(page_list_url)
page_list = json.loads(page_list.text)
print(page_list)
# total_count = len(page_list['data'])
videos_location = os.path.dirname(__file__) + '/videos/' + av_id
if not os.path.exists(videos_location):
    os.mkdir(videos_location)
    print('正在创建本地文件夹: ' + videos_location)
for item in page_list['data']:
    print('正在下载第' + str(item['page']) + '部视频:' + item['part'])
    page_url_prefix = xml['websites']['bilibili']['get-page-url-prefix']
    get_page_url = page_url_prefix.replace('CID_PLACEHOLDER', str(item['cid']))
    print("正在向bilibili9发送请求, 请求地址: " + get_page_url)
    video_json = json.loads(requests.get(get_page_url).text)
    print(video_json)
    video_name = item['part'] + '.mp4'
    print('视频源地址: ' + video_json['Result']['Url']['Main'])
    print('视频存放地址: ' + videos_location + video_name)
    try:
        response = urllib.request.urlretrieve(video_json['Result']['Url']['Main'])
    except Exception as e:
        print(e)
    print(av_id)
