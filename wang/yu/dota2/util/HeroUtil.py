import requests
from bs4 import BeautifulSoup
import xlsxwriter
import os


class HeroUtil:
    def __init__(self):
        self.cell_format = ''
        self.row = 0

    def crawl_dota_hero_info(self):
        url = 'http://db.178.com/dota2/hero-list/'
        hero_temp_url = 'http://db.178.com/dota2/'
        utf_encoding = 'UTF-8'
        path = os.path.dirname(os.path.dirname(__file__)) + '/reports/'
        workbook = xlsxwriter.Workbook(path + 'dota2-heroes-reports.xlsx')
        self.cell_format = workbook.add_format()
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
                    self.create_excel(worksheet, [name, roleshow, '', self.format_long_text(background_div.text), 'to be developed'])
                for spell_div in hero_soup.findAll('div', {'class': 'box_465 bt_12 l'}):
                    spell_name = spell_div.find('h3').text
                    spell_desc = spell_div.find('p').text
                    print('generating hero skill row: ', spell_name)
                    self.create_excel(worksheet, ['', '', spell_name, self.format_long_text(spell_desc), ''])
        finally:
            workbook.close()

    def create_excel(self, worksheet, text):
        self.cell_format.set_align('center')
        self.cell_format.set_align('vcenter')
        if self.row == 0:
            worksheet.write(0, 0, '英雄', self.cell_format)
            worksheet.write(0, 1, '定位', self.cell_format)
            worksheet.write(0, 2, '技能', self.cell_format)
            worksheet.write(0, 3, '描述', self.cell_format)
            worksheet.write(0, 4, '地理位置', self.cell_format)
            self.row += 1
        worksheet.set_column(0, 2, max(len(text[0]), len(text[1]), len(text[2])), self.cell_format)
        worksheet.write(self.row, 0, text[0], self.cell_format)
        worksheet.write(self.row, 1, text[1], self.cell_format)
        worksheet.write(self.row, 2, text[2], self.cell_format)

        worksheet.set_column(3, 3, len(text[3]), self.cell_format)
        worksheet.write(self.row, 3, text[3], self.cell_format)
        worksheet.set_column(4, 4, len(text[4]), self.cell_format)
        worksheet.write(self.row, 4, text[4], self.cell_format)
        self.row += 1

    def format_long_text(self, text):
        return '\n'.join([text[i:i+100] for i in range(0, len(text), 100)])
