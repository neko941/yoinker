# import os
# import csv
# import json
# import time
# import random
# import requests
# import pandas as pd
# from datetime import datetime
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# def next_url(url):
#     try:
#         return [a.find(name='a').get('href') for a in BeautifulSoup(requests.get(url).content, "html.parser").find(name='div', class_='zone--timeline').find(name='nav', class_='pag').findAll(name='li')][-1]
#     except:
#         return None

# class ThanhNienGetURLs():
#     def __init__(self, url):
#         self.url = url
#         self.response = requests.get(url)
#         if self.response.status_code == 200:
#             self.get_soup()
#         self.sub_urls = []

#     def get_soup(self):
#         self.soup = BeautifulSoup(self.response.content, "html.parser")

#     def get_main_sub(self):
#         try:
#             self.sub_urls.extend(urljoin(self.url, parent.find(name="a", class_="story__thumb").get('href')) for parent in self.soup.find(class_="l-content").findAll(name='article', class_="story"))
#         except:
#             return None

#     def get_relative_sub(self):
#         try:
#             self.sub_urls.extend(urljoin(self.url, parent.find(name="a", class_="story__thumb").get('href')) for parent in self.soup.find(class_="relative").findAll(name='article', class_="story"))
#         except:
#             return None

#     def get_hot_sub(self):
#         try:
#             self.sub_urls.extend(urljoin(self.url, parent.find(name="a", class_="story__thumb").get('href')) for parent in self.soup.find(class_="area area--light has-margin").findAll(name='article', class_="story"))  
#         except:
#             return None

#     def get_sub_urls(self):
#         print(self.url)
#         if '/?trang=' not in self.url:
#             self.get_main_sub()
#             self.get_hot_sub() 
#         self.get_relative_sub()
        
#         return self.sub_urls
        

# class ThanhNienScraper():
#     def __init__(self, url):
#         self.url = url
#         self.bug = 0

#         user_agent_list = [
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
#             ]
#         try:
#             self.request_timeout = 0
#             self.response = requests.get(url, headers={'User-Agent': random.choice(user_agent_list)}, timeout=5)
#             if self.response.status_code == 200: self.get_soup()
#         except:
#             self.request_timeout = 1
#             self.log('Request Timeout')
#             print('Request Timeout')

#     def get_soup(self):
#         self.soup = BeautifulSoup(self.response.content, "html.parser")
        
#     def get_datetime(self):
#         try:
#             self.datetime =  self.soup.find(name='div', class_="meta").find(name='time').get('datetime')
#             return self.datetime
#         except:
#             self.bug = 1
#             self.log('Datetime')
#             return None

#     def get_author(self):
#         try:
#             self.author = self.soup.find(name='div', class_="details__author").find(name='div', class_='details__author__meta').find(name='a').get('title')
#         except:
#             self.author = ''
#             self.log('Author')

#     def get_title(self):
#         try:
#             self.title = self.soup.find(name='h1', class_="details__headline cms-title").get_text().strip()
#         except:
#             try:
#                 self.title = self.soup.find(name='h2', class_="details__headline cms-title").get_text().strip()
#             except:
#                 self.bug = 1
#                 self.log('Title')

#     def get_abstract(self):
#         try:
#             self.abstract =  self.soup.find(id='chapeau').get_text().strip()
#         except:
#             self.bug = 1
#             self.log('Abstract')
            
#     def get_content(self):
#         try:
#             for script in self.soup.findAll(name='table', class_='picture'):
#                 script.decompose()
#             for script in self.soup.findAll(name='table', class_='video'):
#                 script.decompose()
#             for script in self.soup.findAll(name='strong'):
#                 if script.get_text() == 'Xem thêm': script.parent.decompose()
#             self.content = "\n".join([a.get_text() for a in self.soup.find(id='abody').findAll(name='p')])
#         except:
#             self.bug = 1
#             self.log('Content')
            
#     def get_tags(self):
#         try:
#             self.tags = [a.get('title').strip() if a.get('title').strip().isupper() else a.get('title').strip().title() for a in self.soup.find(id='abde').find(name='div', class_='details__tags').findAll(name='a')]
#         except:
#             self.bug = 1
#             self.log('Tags')
            
#     def log(self, message, log_dir='error_log'):
#         advanced_mkdir(log_dir)
#         with open(f'{os.path.join(log_dir, datetime.now().strftime("%y-%m-%d"))}.txt', 'a') as f:
#             f.write(f'{datetime.now().strftime("%H:%M:%S")} - {self.url} - {message}\n')

#     def save(self, folder='data'):
#         if self.request_timeout == 0:
#             print(f'Fetching => {self.url}')
            
#             self.get_title()
#             self.get_datetime()
#             self.get_author()
#             self.get_abstract()
#             self.get_content()
#             self.get_tags()

#             if self.bug == 0:
#                 data_file = advanced_path_join([folder, self.datetime[:4], self.url.split('/')[-1].replace('.html', '').split('-')[-1].replace('post', '') + '.json'])
                
#                 # if os.path.exists(data_file):
#                 #     print(f'File exists => {advanced_path_join(data_file)}', end='\n\n')
#                 #     return 

#                 advanced_mkdir(advanced_path_join([folder, self.datetime[:4]]))
                
#                 data = {
#                     'url' : self.url,
#                     'file' : [folder, self.datetime[:4], self.url.split('/')[-1].replace('.html', '').split('-')[-1].replace('post', '') + '.json'],
#                     'title' : self.title,
#                     'datetime' : self.datetime,
#                     'author' : self.author,
#                     'abstract' : self.abstract,
#                     'content' : self.content,
#                     'tags' : self.tags,
#                 }
#                 with open(data_file, 'w', encoding='utf8') as fp:
#                     json.dump(data, fp, indent=4, sort_keys=False, ensure_ascii=False) 
#                 print(f'Data written => {advanced_path_join(data_file)}', end='\n\n')
#             else:
#                 print(f'Errors => {self.url}', end='\n\n') 
        

# def advanced_flatten_list(alist):
#     flattened_list = []
#     for element in alist:
#         if isinstance(element, list):
#             flattened_list.extend(advanced_flatten_list(element))
#         else:
#             flattened_list.append(element)
#     return flattened_list

# def advanced_path_join(alist):
#     if isinstance(alist, list): 
#         if len(alist) > 1:
#             return os.path.join(*advanced_flatten_list(alist))
#         elif len(alist) == 1:
#             return alist[0]
#         else:
#             return ''
#     else:
#         return str(alist)

# def _advanced_mkdir(func):
#     def wrap(a):
#         if isinstance(a, list):
#             func(a)
#         else:
#             func([a])
#     return wrap

# @_advanced_mkdir
# def advanced_mkdir(dir_list):
#     for dir in dir_list:
#         dirs = []
#         while True:
#             if not os.path.exists(dir) and dir != '':
#                 arr = os.path.normpath(dir).split(os.sep)
#                 dirs.insert(0, arr[-1])
#                 dir = advanced_path_join(arr[:-1])
#             else:
#                 for i in range(len(dirs)):
#                     os.mkdir(advanced_path_join([dir, dirs[:i+1]]))
#                 break

# def read(file):
#     if os.path.exists(file):
#         return [line.strip().replace('\n', '') for line in open(file, 'r').readlines()]
#     else:
#         with open(file, 'w') as fp:
#             pass
#         return []

# def write(file, data):
#     with open(file, 'w') as fp:
#         for item in data:
#             fp.write("%s\n" % item)

def fix_csv(file_name, sort_by_column=None):
    df = pd.read_csv(file_name, index_col=0)
    df = df[~df.index.duplicated()]
    if sort_by_column != None:
        df.sort_values(by=[sort_by_column], ascending=False)
    df.to_csv(file_name)

# def get_url(url, save_dir='data', save_file='thanhnien', format='csv'):
#     advanced_mkdir(save_dir)
#     while True:
#         sub_urls = ThanhNienGetURLs(url).get_sub_urls()
        
#         if sub_urls == None: break
#         data_file = os.path.join(save_dir, f'{save_file}.{format}')
#         if format == 'txt':
#             data = read()
#             data.extend(sub_urls)
#             data.sort()
#             data = list(set(data))
#             write(os.path.join(save_dir, save_file), data)
#             [print(f'Write => {u}') for u in sub_urls]
#         elif format == 'csv':
#             if not os.path.exists(data_file):
#                 with open(data_file, 'a+', newline='') as file:
#                     csv.writer(file).writerow(['file_name', 'url', 'year'])
            
#             data = pd.read_csv(data_file)
            
#             for sub_url in sub_urls:
#                 year = ThanhNienScraper(sub_url).get_datetime()
#                 file_name = sub_url.split('/')[-1].replace('.html', '').split('-')[-1].replace('post', '') + '.json'
#                 if year == None: continue
#                 info = [file_name, sub_url, year[:4]]
#                 with open(data_file, 'a+', newline='') as file:
#                     writer = csv.writer(file)
#                     if not data.loc[(data['file_name'] == file_name) & (data['url'] == sub_url) & (data['year'] == year[:4])].any().all():
#                         writer.writerow(info)
#                 print(f'Write => {sub_url}')
#         fix_csv(data_file, sort_by_column='file_name')
#         url = next_url(url)
#         time.sleep(1)
#         print()
#         if url == None: break

# def file_txt_to_list(file_name, duplicate=False, remove_new_line_char=True, shuffle=False, sort=None):
#     lines = []
#     for line in open(file_name, 'r').readlines():
#         if remove_new_line_char:
#             line = line.replace('\n', '')
#         lines.append(line)
#     if duplicate: lines = list(set(lines))
#     if shuffle: random.shuffle(lines)
#     if sort != None:
#         if sort.lower() in ['ascending', 'asc']: lines.sort()
#         elif sort.lower() in ['descending', 'desc']: lines.sort(reverse=True)
#     return lines

# if __name__ == "__main__":
#     # for i in range(100):
#     #     for url in file_txt_to_list(file_name='pages.txt', shuffle=True):
#     #         get_url(url)

#     for url in [
#         'https://thanhnien.vn/the-gioi/', 
#         'https://thanhnien.vn/thoi-su/', 
#         'https://thanhnien.vn/tai-chinh-kinh-doanh/', 
#         'https://thanhnien.vn/doi-song/',
#         'https://thanhnien.vn/du-lich/',
#         'https://thanhnien.vn/van-hoa/',
#         'https://thanhnien.vn/giai-tri/',
#         'https://thanhnien.vn/gioi-tre/',
#         'https://thanhnien.vn/giao-duc/',
#         'https://thanhnien.vn/the-thao/',
#         'https://thanhnien.vn/suc-khoe/']:
#         get_url(url)
#     # with open(os.path.join('data', 'thanhnien.csv'), newline='') as f:
#     #     reader = csv.reader(f)
#     #     data_dir = 'data'
#     #     for idx, row in enumerate(reader):
#     #         print(f'Count: {idx}')
#     #         if row == ['file_name', 'url', 'year']:
#     #             continue

#     #         file_path = [data_dir, row[2], row[0]]
#     #         if not os.path.exists(advanced_path_join(file_path)):
#     #             ThanhNienScraper(row[1]).save(data_dir)
#     #         else:
#     #             print(f'File exists => {advanced_path_join(file_path)}', end='\n\n')

import os
import csv
import json
import time
import random
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
        self.sub_urls = []

    def get_soup(self):
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def get_main_sub(self):
        try:
            self.sub_urls.extend(urljoin(self.url, parent.find(name="a", class_="story__thumb").get('href')) for parent in self.soup.find(class_="l-content").findAll(name='article', class_="story"))
        except:
            return None

    def get_relative_sub(self):
        try:
            self.sub_urls.extend(urljoin(self.url, parent.find(name="a", class_="story__thumb").get('href')) for parent in self.soup.find(class_="relative").findAll(name='article', class_="story"))
        except:
            return None

    def get_hot_sub(self):
        try:
            self.sub_urls.extend(urljoin(self.url, parent.find(name="a", class_="story__thumb").get('href')) for parent in self.soup.find(class_="area area--light has-margin").findAll(name='article', class_="story"))  
        except:
            return None

    def get_sub_urls(self):
        print(self.url)
        if '/?trang=' not in self.url:
            self.get_main_sub()
            self.get_hot_sub() 
        self.get_relative_sub()
        
        return self.sub_urls
        

class ThanhNienScraper():
    def __init__(self, url):
        self.url = url
        self.bug = 0

        user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            ]
        try:
            self.response = requests.get(url, headers={'User-Agent': random.choice(user_agent_list)}, timeout=5)
        except:
            self.bug = 1
            self.log('Request Timeout')

        if self.response.status_code == 200: self.get_soup()

    def get_soup(self):
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        
    def get_datetime(self):
        try:
            
            self.datetime =  self.soup.find(name='div', class_="meta").find(name='time').get('datetime')
            return self.datetime
        except:
            self.bug = 1
            self.log('Datetime')

    def get_author(self):
        try:
            self.author = self.soup.find(name='div', class_="details__author").find(name='div', class_='details__author__meta').find(name='a').get('title')
        except:
            self.bug = 1
            self.log('Author')

    def get_title(self):
        try:
            self.title = self.soup.find(name='h1', class_="details__headline cms-title").get_text().strip()
        except:
            self.bug = 1
            self.log('Title')

    def get_abstract(self):
        try:
            self.abstract =  self.soup.find(id='chapeau').get_text().strip()
        except:
            self.bug = 1
            self.log('Abstract')
            
    def get_content(self):
        try:
            for script in self.soup.findAll(name='table', class_='picture'):
                script.decompose()
            for script in self.soup.findAll(name='table', class_='video'):
                script.decompose()
            for script in self.soup.findAll(name='strong'):
                if script.get_text() == 'Xem thêm': script.parent.decompose()
            self.content = "\n".join([a.get_text() for a in self.soup.find(id='abody').findAll(name='p')])
        except:
            self.bug = 1
            self.log('Content')
            
    def get_tags(self):
        try:
            self.tags = [a.get('title').strip() if a.get('title').strip().isupper() else a.get('title').strip().title() for a in self.soup.find(id='abde').find(name='div', class_='details__tags').findAll(name='a')]
        except:
            self.bug = 1
            self.log('Tags')
            
    def log(self, message, log_dir='error_log'):
        advanced_mkdir(log_dir)
        with open(f'{os.path.join(log_dir, datetime.now().strftime("%y-%m-%d"))}.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} - {self.url} - {message}\n')

    def save(self, folder):
        print(f'Fetching => {self.url}')
        
        self.get_title()
        self.get_datetime()
        self.get_author()
        self.get_abstract()
        self.get_content()
        self.get_tags()

        advanced_mkdir(advanced_path_join([folder, self.datetime[:4]]))

        data_file = advanced_path_join([folder, self.datetime[:4], self.url.split('/')[-1].replace('.html', '').split('-')[-1].replace('post', '') + '.json'])
        
        if os.path.exists(data_file):
            print(f'File exists => {advanced_path_join(data_file)}', end='\n\n')
            return 

        if self.bug == 0:
            data = {
                'url' : self.url,
                'title' : self.title,
                'datetime' : self.datetime,
                'author' : self.author,
                'abstract' : self.abstract,
                'content' : self.content,
                'tags' : self.tags,
            }
            with open(data_file, 'w', encoding='utf8') as fp:
                json.dump(data, fp, indent=4, sort_keys=False, ensure_ascii=False) 
            print(f'Data written => {advanced_path_join(data_file)}', end='\n\n')
        else:
            print(f'Errors => {self.url}', end='\n\n') 
        

def advanced_flatten_list(alist):
    flattened_list = []
    for element in alist:
        if isinstance(element, list):
            flattened_list.extend(advanced_flatten_list(element))
        else:
            flattened_list.append(element)
    return flattened_list

def advanced_path_join(alist):
    if isinstance(alist, list): 
        if len(alist) > 1:
            return os.path.join(*advanced_flatten_list(alist))
        elif len(alist) == 1:
            return alist[0]
        else:
            return ''
    else:
        return str(alist)

def _advanced_mkdir(func):
    def wrap(a):
        if isinstance(a, list):
            func(a)
        else:
            func([a])
    return wrap

@_advanced_mkdir
def advanced_mkdir(dir_list):
    for dir in dir_list:
        dirs = []
        while True:
            if not os.path.exists(dir) and dir != '':
                arr = os.path.normpath(dir).split(os.sep)
                dirs.insert(0, arr[-1])
                dir = advanced_path_join(arr[:-1])
            else:
                for i in range(len(dirs)):
                    os.mkdir(advanced_path_join([dir, dirs[:i+1]]))
                break

def read(file):
    if os.path.exists(file):
        return [line.strip().replace('\n', '') for line in open(file, 'r').readlines()]
    else:
        with open(file, 'w') as fp:
            pass
        return []

def write(file, data):
    with open(file, 'w') as fp:
        for item in data:
            fp.write("%s\n" % item)

def get_url(url, save_dir='data', save_file='thanhnien', format='csv'):
    advanced_mkdir(save_dir)
    while True:
        sub_urls = ThanhNienGetURLs(url).get_sub_urls()
        
        if sub_urls == None: break
        data_file = os.path.join(save_dir, f'{save_file}.{format}')
        if format == 'txt':
            data = read()
            data.extend(sub_urls)
            data.sort()
            data = list(set(data))
            write(os.path.join(save_dir, save_file), data)
            [print(f'Write => {u}') for u in sub_urls]
        elif format == 'csv':
            if not os.path.exists(data_file):
                with open(data_file, 'a+', newline='') as file:
                    csv.writer(file).writerow(['file_name', 'url', 'year'])
            
            data = pd.read_csv(data_file)
            
            for sub_url in sub_urls:
                year = ThanhNienScraper(sub_url).get_datetime()
                file_name = sub_url.split('/')[-1].replace('.html', '').split('-')[-1].replace('post', '') + '.json'
                if year == None: continue
                info = [file_name, sub_url, year[:4]]
                with open(data_file, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    if not data.loc[(data['file_name'] == file_name) & (data['url'] == sub_url) & (data['year'] == year[:4])].any().all():
                        writer.writerow(info)
                print(f'Write => {sub_url}')
        fix_csv(data_file, sort_by_column='file_name')
        url = next_url(url)
        time.sleep(1)
        print()
        if url == None: break

# def file_txt_to_list(file_name, duplicate=False, remove_char=['\n']):
#     for line in open('pages.txt', 'r').readlines():


if __name__ == "__main__":
    # print(type(open('pages.txt', 'r').readlines()))
    # for url in open('pages.txt', 'r').readlines():
    #     print(url)

    for url in ['https://thanhnien.vn/the-gioi/', 
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
        get_url(url)

    # for url in read(advanced_path_join(['data', 'thanhnien.txt'])):
    #     time.sleep(1)
    #     ThanhNienScraper(url).save('data')
    # print(ThanhNienScraper('https://thanhnien.vn/tu-cuoc-chien-o-ukraine-nhin-lai-kho-uav-cua-iran-post1501580.html').get_datetime())