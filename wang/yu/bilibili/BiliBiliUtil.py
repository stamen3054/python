import json
import os
import time

import requests

from wang.yu.common.PyXmlParser import PyXmlParser


class BiliBiliUtil:
    def __init__(self):
        py_xml_parser = PyXmlParser(os.path.dirname(os.path.dirname(__file__)) + '/common/properties/properties.xml')
        self.xml = py_xml_parser.do_parse()

    def download_videos(self):
        headers = {
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/video/%s/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/46.0.2490.80 Safari/537.36]'
        }
        page_list_prefix = self.xml['websites']['bilibili']['page-list-prefix']
        av_id = input('输入av号:\n')
        page_list_url = page_list_prefix % av_id
        page_list = requests.get(page_list_url)
        page_list = json.loads(page_list.text)
        if page_list['code'] != 0:
            raise NameError('错误的番号: %s' % av_id)
        else:
            videos_location = os.path.dirname(__file__) + '/videos/%s/' % av_id
            headers['referer'] = headers['referer'] % ('av' + av_id)
            failed_items = []
            success_items = []
            duplicate_items = []
            print('=====================================================================')
            if not os.path.exists(videos_location):
                os.mkdir(videos_location)
                print('正在创建本地文件夹: ' + videos_location)
                print('=====================================================================')
            for item in page_list['data']:
                try:
                    print('正在下载第' + str(item['page']) + '部视频: ' + item['part'])
                    page_url_prefix = self.xml['websites']['bilibili']['get-page-url-prefix']
                    get_page_url = page_url_prefix % str(item['cid'])
                    print("正在向bilibili9发送请求, 请求地址: " + get_page_url)
                    video_json = json.loads(requests.get(get_page_url).text)
                    video_name = item['part']
                    video_type = video_json['Result']['Url']['Main'].split('/')[7].split('.')[1].split('?')[0]
                    video_name += '.' + video_type
                    if os.path.exists(videos_location + video_name):
                        duplicate_items.append(video_name)
                        print('已经存在, 跳过下载，')
                    else:
                        print('视频源地址: %s' % video_json['Result']['Url']['Main'])
                        print('视频存放地址: %s' % videos_location + video_name)
                        requests.adapters.DEFAULT_RETRIES = 5
                        s = requests.session()
                        s.keep_alive = False
                        response = s.get(video_json['Result']['Url']['Main'], headers=headers)
                        if response.status_code != 200:
                            raise Exception('请求返回值%s' % response.status_code)
                        else:
                            with open(videos_location + video_name, 'wb') as file:
                                for data in response.iter_content(chunk_size=1024):
                                    file.write(data)
                                    file.flush()
                                success_items.append(video_name)
                                print('成功下载: %s\n存放于: %s' % (video_name, videos_location))
                except Exception as e:
                    failed_items.append(video_name)
                    print('无法下载%s, 原因: %s' % (video_name, e))
                finally:
                    print('=====================================================================')
            print('完成, 以下内容下载成功:')
            print('\n'.join(item for item in success_items))
            print('=====================================================================')
            print('以下内容已存在于本地:')
            print('\n'.join(item for item in duplicate_items))
            print('=====================================================================')
            print('以下内容下载失败:')
            print('\n'.join(item for item in failed_items))

    def user_age_graph(self):
        headers = {
            'referer': 'https://space.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/68.0.3440.106 Safari/537.36'
        }
        sex_list=[]

        get_user_info_url = self.xml['websites']['bilibili']['get-user-info-url']
        max_num = 20000000
        for user_id in range(1, max_num):
            response = requests.post(get_user_info_url, data={'mid': user_id}, headers=headers)
            user_json = json.loads(response.text)
            # 每100个用户休息10秒，以防被禁ip
            if user_id % 100 == 0:
                time.sleep(10)
            if user_json['status']=='False':
                print('无效的用户:%s' % user_id)
            else:
                print('成功获取用户id:%s' % user_id)

            print(user_json)
