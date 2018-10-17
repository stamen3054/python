import os

import requests
from bs4 import BeautifulSoup

from wang.yu.common.PyXmlParser import PyXmlParser


class BossUtil:
    def __init__(self):
        py_xml_parser = PyXmlParser(os.path.dirname(os.path.dirname(__file__)) + '/common/properties/properties.xml')
        self.xml = py_xml_parser.do_parse()['websites']['boss']

    def fetch_job_list_by_city(self):
        city_code = input('输入城市代码（默认为天津101030100）：') or '101030100'
        headers = {
            'referer': 'https://www.zhipin.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/69.0.3497.100 Safari/537.36',
        }

        fetch_job_list_url = self.xml['fetch-job-list-url']
        job_list = []
        count = 0
        index = 0
        has_next = True
        while has_next:
            count += 1
            print('正在获取第%s页信息...' % count)
            job_list_url = fetch_job_list_url % (city_code, city_code, count, count)
            fetch_job_list_page = requests.get(job_list_url, headers=headers)
            plain_text = fetch_job_list_page.text
            soup = BeautifulSoup(plain_text, 'html.parser')
            for job_info_div in soup.select('div.info-primary'):
                job_info = []
                job_detail_url = self.xml['job-detail-url-prefix'] % job_info_div.select_one('a')['href']
                job_title = job_info_div.select_one('div.job-title').text
                job_salary = job_info_div.select_one('span.red').text
                job_info.append(job_detail_url)
                job_info.append(job_title)
                job_info.append(job_salary)
                job_list.append(job_info)
            for company_info_div in soup.select('div.info-company'):
                company_name = company_info_div.select_one('h3 a').text
                company_url = self.xml['company-url-prefix'] % company_info_div.select_one('h3 a')['href']
                job_list[index].append(company_name)
                job_list[index].append(company_url)
                index += 1
            # 最后一页的下一页按钮是disable的
            next_btn = soup.findAll('a', {'ka': 'page-next'})
            for attr in next_btn[0]['class']:
                if attr == 'disabled':
                    has_next = False
                    print('完成全部爬取')
        print('\n'.join(', '.join(job) for job in job_list))
