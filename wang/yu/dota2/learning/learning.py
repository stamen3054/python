import requests
from bs4 import BeautifulSoup
import xlsxwriter


def crawl_dota_hero_info():
    global maxWidth0, maxWidth1, maxWidth2, maxWidth3, maxWidth4
    max_length = 50
    url = 'http://db.178.com/dota2/hero-list/'
    hero_temp_url = 'http://db.178.com/dota2/'
    utf_encoding = 'UTF-8'
    workbook = xlsxwriter.Workbook('dota2.xlsx')
    cell_format = workbook.add_format()
    worksheet = workbook.add_worksheet('hero info')
    try:
        source_code = requests.get(url)
        source_code.encoding = utf_encoding
        plain_text = source_code.text
        overview_soup = BeautifulSoup(plain_text, 'html.parser')
        for anchor in overview_soup.findAll('a', {'class': 'hero_overview_grid'}):
            hero_url = hero_temp_url + anchor.get('href')[7:]
            print('accessing hero page: ', hero_url)
            hero_detail_page = requests.get(hero_url)
            hero_detail_page.encoding = utf_encoding
            hero_detail_text = hero_detail_page.text
            hero_soup = BeautifulSoup(hero_detail_text)
            name = anchor.get('title')
            roleshow = anchor.get('roleshow')
            for background_div in hero_soup.findAll('div', {'class': 'box_b_in p5 text_2'}):
                print('generating hero row: ', name)
                create_excel(worksheet, [name, roleshow, '', background_div.text, 'to be developed'])
            for spell_div in hero_soup.findAll('div', {'class': 'box_465 bt_12 l'}):
                spell_name = spell_div.find('h3').text
                spell_desc = spell_div.find('p').text
                print('generating hero skill row: ', spell_name)
                create_excel(worksheet, ['', '', spell_name, spell_desc, ''])
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        worksheet.set_column(0, 0, 2.2 * maxWidth0, cell_format)
        worksheet.set_column(1, 1, 2.2 * maxWidth1, cell_format)
        worksheet.set_column(2, 2, 2.2 * maxWidth2, cell_format)
        cell_format = workbook.add_format()
        cell_format.set_align('vcenter')
        cell_format.set_text_wrap()
        cell_format.set_align('left')
        worksheet.set_column(3, 3, 2.2 * max_length, cell_format)
        worksheet.set_column(4, 4, 2.2 * max_length, cell_format)
    finally:
        workbook.close()


def create_excel(worksheet, text):
    global row, maxWidth0, maxWidth1, maxWidth2, maxWidth3, maxWidth4
    maxWidth0 = max(len(text[0]), maxWidth0)
    maxWidth1 = max(len(text[1]), maxWidth1)
    maxWidth2 = max(len(text[2]), maxWidth2)
    maxWidth3 = max(len(text[3]), maxWidth3)
    maxWidth4 = max(len(text[4]), maxWidth4)
    if row == 0:
        worksheet.write(0, 0, '英雄')
        worksheet.write(0, 1, '定位')
        worksheet.write(0, 2, '技能')
        worksheet.write(0, 3, '描述')
        worksheet.write(0, 4, '地理位置')
        row += 1
    worksheet.write(row, 0, text[0])
    worksheet.write(row, 1, text[1])
    worksheet.write(row, 2, text[2])
    worksheet.write(row, 3, text[3])
    worksheet.write(row, 4, text[4])
    row += 1


def format_long_text(text, max_length):
    return '\n'.join([text[i:i+max_length] for i in range(0, len(text), max_length)])


row = 0
maxWidth0 = 0
maxWidth1 = 0
maxWidth2 = 0
maxWidth3 = 0
maxWidth4 = 0
crawl_dota_hero_info()

