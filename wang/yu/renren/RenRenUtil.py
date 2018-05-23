import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import os

album_list_url_prefix = 'http://photo.renren.com/photo/<user_id>/albumlist/v7?offset=0'
album_url_prefix = 'http://photo.renren.com/photo/<user_id>/album-<album_id>/v7'
photo_url_prefix = 'http://photo.renren.com/photo/<user_id>/album-<album_id>' \
                   '/bypage/ajax/v7?page=<page_number>&pageSize=<page_size>'
item_list_selector = 'script'
image_path_prefix = os.path.dirname(__file__) + '/images/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'anonymid=jbxt1sweqy9qxs; _r01_=1; _de=EFF6C4BFE8062CA9A8DA1F0D724762818ED172744450A224; depovince=GW;'
              ' p=7d5a7d53c319f9f571aa5f75812546736; ap=251796516; ln_uact=wangyu3054@163.com; ln_hurl=http://hdn.xni'
              'mg.cn/photos/hdn321/20120102/0015/h_main_BXw0_7a8300022ac72f75.jpg; jebe_key=7d64dd11-e9f1-4ef9-a298-'
              'c0b697396041%7Ccc843828bb292f8c71cbd1588ed4e6b5%7C1526999742393%7C1%7C1526999744209; __utma=10481322.'
              '1689172147.1527001217.1527001217.1527001217.1; __utmz=10481322.1527001217.1.1.utmcsr=(direct)|utmccn=('
              'direct)|utmcmd=(none); _ga=GA1.2.1689172147.1527001217; _gid=GA1.2.1554020109.1527019342; first_login_'
              'flag=1; t=b1a26f6151e515ee1126ef34721906f56; societyguester=b1a26f6151e515ee1126ef34721906f56; id=25179'
              '6516; xnsid=72c8b90f; ver=7.0; ',
    'Host': 'photo.renren.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/66.0.3359.181 Safari/537.36'
}

user_id = input("Enter your user_id:")
source_code = requests.get(album_list_url_prefix.replace('<user_id>', user_id), headers=headers)
plain_text = source_code.text
overview_soup = BeautifulSoup(plain_text, 'html.parser')
album_list_script = overview_soup.select(item_list_selector)[5]
album_list_text = str(album_list_script).split('nx.data.photo = ')[1].split(';\nnx.data.hasHiddenAlbum')[0]\
    .replace('\'', '"')
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
    album_source_code = requests.get(album_url, headers=headers)
    if album_source_code.status_code == 200:
        count = 0
        album_plain_text = album_source_code.text
        album_overview_soup = BeautifulSoup(album_plain_text, 'html.parser')
        photo_list_script = album_overview_soup.select(item_list_selector)[5]
        photo_list_text = str(photo_list_script).split('nx.data.photo = ')[1].split(';\n; define.config(')[0]\
            .replace('\'', '"')
        photo_json = json.loads(photo_list_text)
        photo_count = int(photo_json['photoList']['photoCount'])
        page_number = 1
        page_size = 20
        while count < photo_count:
            photo_url = photo_url_prefix.replace('<user_id>', user_id).replace('<album_id>', album_id)\
                .replace('<page_number>', str(page_number)).replace('<page_size>', str(page_size))
            photo_source_code = requests.get(photo_url, headers=headers)
            photo_plain_text = photo_source_code.text
            photo_json = json.loads(photo_plain_text)
            for photo in photo_json['photoList']:
                count += 1
                photo_url = photo['url']
                photo_id = photo['photoId']
                print('downloading ', count, '/', photo_count, ' photo url: ', photo_url)
                try:
                    urllib.request.urlretrieve(photo_url, image_path + '/' + photo_id + '.jpg')
                except Exception:
                    print('Failed to download photo from album ', album_name, ', photo url: ', photo_url)
            page_number += 1
    else:
        print('Failed to retrieve album ', album_id, ', request returns ', album_source_code.status_code)
        print('album url = ', album_url)
