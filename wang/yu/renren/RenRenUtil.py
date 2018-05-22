import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import os

album_list_url_prefix = 'http://photo.renren.com/photo/<user_id>/albumlist/v7?offset=0'
album_url_prefix = 'http://photo.renren.com/photo/<user_id>/album-<album_id>/v7'
item_list_selector = 'script'
image_path_prefix = os.path.dirname(__file__) + '/images/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'anonymid=jbxt1sweqy9qxs; _r01_=1; _de=EFF6C4BFE8062CA9A8DA1F0D724762818ED172744450A224; depovince=GW; jebecookies=ddb5fac5-9337-4edc-ad3c-c50ce11c5223|||||; ick_login=02600425-0332-4906-85ab-88ddaf9df7b2; p=7d5a7d53c319f9f571aa5f75812546736; ap=251796516; first_login_flag=1; ln_uact=wangyu3054@163.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn321/20120102/0015/h_main_BXw0_7a8300022ac72f75.jpg; t=7ef03541c785ade08f06849fc3079e856; societyguester=7ef03541c785ade08f06849fc3079e856; id=251796516; xnsid=77b9157f; ver=7.0; loginfrom=null; jebe_key=7d64dd11-e9f1-4ef9-a298-c0b697396041%7Ccc843828bb292f8c71cbd1588ed4e6b5%7C1526999742393%7C1%7C1526999744209; wp_fold=0; JSESSIONID=abcB_cWWQsTbW-N3Wriow; __utma=10481322.1689172147.1527001217.1527001217.1527001217.1; __utmc=10481322; __utmz=10481322.1527001217.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'Host': 'photo.renren.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

user_id = input("Enter your user_id:")
source_code = requests.get(album_list_url_prefix.replace('<user_id>', user_id), headers=headers)
plain_text = source_code.text
overview_soup = BeautifulSoup(plain_text, 'html.parser')
album_list_script = overview_soup.select(item_list_selector)[5]
album_list_text = str(album_list_script).split('nx.data.photo = ')[1].split(';\nnx.data.hasHiddenAlbum')[0].replace('\'', '"')
album_json = json.loads(album_list_text)

for album in album_json['albumList']['albumList']:
    album_id = album['albumId']
    album_name = album['albumName']
    image_path = image_path_prefix + user_id
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    image_path = image_path + '/' + album_name + '_' + album_id
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    print('downloading album ', album_name, ' to ', image_path)
    album_url = album_url_prefix.replace('<user_id>', user_id).replace('<album_id>', album_id)
    source_code1 = requests.get(album_url, headers=headers)
    if source_code1.status_code == 200:
        plain_text1 = source_code1.text
        overview_soup1 = BeautifulSoup(plain_text1, 'html.parser')
        photo_list_script = overview_soup1.select(item_list_selector)[5]
        photo_list_text = str(photo_list_script).split('nx.data.photo = ')[1].split(';\n; define.config(')[0].replace('\'', '"')
        photo_json = json.loads(photo_list_text)
        for photo in photo_json['photoList']['photoList']:
            photo_url = photo['url']
            photo_id = photo['photoId']
            urllib.request.urlretrieve(photo_url, image_path + '/' + photo_id + '.jpg')
    else:
        print('Failed to retrieve album ', album_id, ', request returns ', source_code1.status_code)
        print('album url = ', album_url)

