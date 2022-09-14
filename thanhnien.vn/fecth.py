import os
import csv
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# from multiprocessing import Pool

def next_url(url):
    try:
        return [a.find(name='a').get('href') for a in BeautifulSoup(requests.get(url).content, "html.parser").find(name='div', class_='zone--timeline').find(name='nav', class_='pag').findAll(name='li')][-1]
    except:
        return None

class ThanhNienGetURLs():
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        if self.response.status_code == 200:
            self.get_soup()

    def get_soup(self):
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def get_sub_urls(self):
        return [urljoin(self.url, parent.find("a", class_="story__thumb").get('href')) for parent in self.soup.find(class_="relative").findAll(name='article', class_="story")]

class ThanhNienScraper():
    def __init__(self, url):
        self.url = url
        user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            ]
        self.response = requests.get(url, headers={'User-Agent': random.choice(user_agent_list)})
        if self.response.status_code == 200:
            self.get_soup()

    def get_soup(self):
        self.soup = BeautifulSoup(self.response.content, "html.parser")
    
    def get_datetime(self):
        return self.soup.find(name='div', class_="meta").find(name='time').get('datetime')

    def get_author(self):
        return self.soup.find(name='div', class_="details__author").find(name='div', class_='details__author__meta').find(name='a').get('title')

    def get_title(self):
        return self.soup.find(name='h1', class_="details__headline cms-title").get_text().strip()

    def get_abstract(self):
        return self.soup.find(id='chapeau').get_text().strip()

    def get_content(self):
        for script in self.soup.findAll(name='table', class_='picture'):
            script.decompose()
        for script in self.soup.findAll(name='table', class_='video'):
            script.decompose()
        for script in self.soup.findAll(name='strong'):
            if script.get_text() == 'Xem thêm': script.parent.decompose()
        return "\n".join([a.get_text() for a in self.soup.find(id='abody').findAll(name='p')])

    def get_tags(self):
        return [a.get('title').strip() if a.get('title').strip().isupper() else a.get('title').strip().title() for a in self.soup.find(id='abde').find(name='div', class_='details__tags').findAll(name='a')]
    
    def fix(self, file_name):
        df = pd.read_csv(file_name, index_col=0)
        df = df[~df.index.duplicated()]
        df.to_csv(file_name)

    def save(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        data_file = os.path.join(folder, f'{self.get_datetime()[:4]}.csv')
        if not os.path.exists(data_file):
            with open(data_file, 'a+', newline='', encoding="utf-8") as file:
                csv.writer(file).writerow(['url', 'title', 'datetime', 'author', 'abstract', 'content', 'tags'])

        data = pd.read_csv(data_file, engine='python')
        with open(data_file, 'a+', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            if not data.loc[(data['url'] == self.url)].any().all():
                writer.writerow([self.url, self.get_title(), self.get_datetime(), self.get_author(), self.get_abstract(), self.get_content(), self.get_tags()])
                print(f'Saved => {self.url}\n')
            else: 
                print(f'Exists => {self.url}\n')
        
        self.fix(data_file)

def fetch(url):
    while True:
        print(url)
        for u in ThanhNienGetURLs(url).get_sub_urls():
            print(f'Fetching => {u}')
            ThanhNienScraper(u).save('data') 
        
        url = next_url(url)
        time.sleep(1)

        if url == None:
            break

if __name__ == "__main__":
    for url in [
        'https://thanhnien.vn/the-gioi/', 
        'https://thanhnien.vn/thoi-su/', 
        'https://thanhnien.vn/tai-chinh-kinh-doanh/', 
        'https://thanhnien.vn/doi-song/',
        'https://thanhnien.vn/du-lich/',
        'https://thanhnien.vn/van-hoa/',
        'https://thanhnien.vn/giai-tri/',
        'https://thanhnien.vn/gioi-tre/',
        'https://thanhnien.vn/giao-duc/',
        'https://thanhnien.vn/the-thao/',
        'https://thanhnien.vn/suc-khoe/']:
        fetch(url)
    # with Pool(5) as p:
    #     print(p.map(fetch, [
    #     'https://thanhnien.vn/the-gioi/', 
    #     'https://thanhnien.vn/thoi-su/', 
    #     'https://thanhnien.vn/tai-chinh-kinh-doanh/', 
    #     'https://thanhnien.vn/doi-song/',
    #     'https://thanhnien.vn/du-lich/',
    #     'https://thanhnien.vn/van-hoa/',
    #     'https://thanhnien.vn/giai-tri/',
    #     'https://thanhnien.vn/gioi-tre/',
    #     'https://thanhnien.vn/giao-duc/',
    #     'https://thanhnien.vn/the-thao/',
    #     'https://thanhnien.vn/suc-khoe/']))