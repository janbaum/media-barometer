from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET
import dataset
import random
import string
import json

def gen_uniqueId():     # generate unique Identification-Code for each single article
    newId = ''.join(random.choice(string.ascii_letters) for _ in range(16))
    return newId


class FeedParser:
    def __init__(self, url, main_table):
        self.url = url
        self.db = dataset.connect('sqlite:///mydb_3.db')
        self.mt = self.db[main_table]
        self.arguments = ['title', 'link', 'description', 'category', 'pubDate']
        self.id_table = self.db['id_table']
        self.uniqueId = 0

    def get_response(self):
        response = requests.get(self.url)
        return ET.fromstring(response.content)

    def parse_feed(self, **kwargs):
        root = self.get_response()
        for article in root.findall('.channel/item'):

            # Only continue, if article-title not already in db.table[title]
            if not self.mt.find_one(title=article.find('title').text):
                while 1:
                    ID = gen_uniqueId()

                    # If uniquId not already exists in db.id_table[uniqueId] parse arguments
                    if not self.id_table.find_one(uniqueId=ID):
                        self.id_table.insert(dict(uniqueId=ID))
                        arg_dict = {'unique_Id': ID}
                        for a in self.arguments:
                            try:
                                arg = article.find(a).text
                                arg_dict[a] = arg
                            except AttributeError:        # AttrErr in case of None-type
                                arg_dict[a] = None

                        for kw in kwargs:                 # also include given arguments from main.get_feed(...)
                            keyword = article.find(kw)    # for example get_feed(tags='tags')
                            arg_dict[kw] = keyword
                        arg_dict['scraped'] = False

                        self.mt.insert(arg_dict)          # insert all found arguments as one dict in given table
                        break
                    else:
                        continue


class Scraper:
    def __init__(self, main_table):
        self.db = dataset.connect('sqlite:///mydb_3.db')
        self.main_table = self.db[main_table]

    # tag_class='meta', attributes=['author', 'news_keywords']
    def add_author_and_tags(self, tag_class, attributes):
        # faz_articles = db['faz_main_table'].find(scraped=0)
        not_scraped_articles = self.main_table.find(scraped=0)
        for article in not_scraped_articles:
            # If 'scraped'-value == 0, go scraping
            if article['scraped'] == 0:
                link = article['link']
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                for att in attributes:
                    try:
                        meta_tag = soup.find(tag_class, attrs=att)
                        content = meta_tag["content"]
                        key_name = list(att.keys())
                        self.main_table.update({'id': article['id'], 'scraped': 1, att[key_name[0]]: content}, ['id'])
                    except TypeError:
                        content = 'NV'
                        key_name = list(att.keys())
                        self.main_table.update({'id': article['id'], 'scraped': 1, att[key_name[0]]: content}, ['id'])

    def faz_scraper(self):

        not_scraped_articles = self.main_table.find(author='Frankfurter Allgemeine Zeitung GmbH')
        for article in not_scraped_articles:
            link = article['link']
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            div_element = soup.find('div', {'class': 'js-adobe-digital-data'})
            data = div_element['data-digital-data']
            json_data = json.loads(data)
            author_name = json_data['article']['author']
            if author_name == 'ohne Author':
                author_name = 'NV'
            self.main_table.update({'id': article['id'], 'author': author_name}, ['id'])
