import os
import csv
import time
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup

from utils import isfloat
from utils import flatten_list

class Writting9GetLinks():
    def __init__(self, bands):
        self.bands = bands
        self.info = []

    def get_sub_urls(self, url):
        return flatten_list([[f"https://writing9.com{a.get('href')}" for a in item.find_all('a', href=True)] for item in BeautifulSoup(requests.get(url).content, "html.parser").findAll(name='div', class_='jsx-2609154510 item')])
    
    def fix(self, file_name):
        df = pd.read_csv(file_name, index_col=0)
        df = df[~df.index.duplicated()]
        df.to_csv(file_name)

    def log(self, url, message, log_dir='error_log'):
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        with open(f'{os.path.join(log_dir, datetime.now().strftime("%y-%m-%d"))}.txt' , 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} - {url} - {message}\n')

    def get_urls(self, save=True, name='writing9', format='csv'):
        for band in self.bands:
            total_pages = int([a.get_text() for a in BeautifulSoup(requests.get(f'https://writing9.com/band/{band}/0').content, "html.parser").find(name='ul', class_='items').findAll(name='a', class_='item')][-2])
            print(f'\nFETCHING BAND {band}')
            for page in tqdm(range(total_pages)):
                url = f'https://writing9.com/band/{band}/{page}'
                response = requests.get(url)
                time.sleep(1)
                if response.status_code == 200:
                    sub_urls = self.get_sub_urls(url)
                    if len(sub_urls) == 0:
                        self.log(url, "Sub URLs")
                    else:
                        if save:
                            assert name, format
                            data_file = f'{name}.{format}'
                            if format == 'csv':
                                if not os.path.exists(data_file):
                                    with open(data_file, 'a+', newline='') as file:
                                        csv.writer(file).writerow(['url', 'band', 'file_name'])
                                
                                data = pd.read_csv(data_file)
                                
                                for sub_url in sub_urls:
                                    info = [sub_url, str(band).replace('.', ''), sub_url.split('/')[-1].split('-')[0] + '.json']
                                    with open(data_file, 'a+', newline='') as file:
                                        writer = csv.writer(file)
                                        if not data.loc[(data['url'] == sub_url) & (data['band'] == band) & (data['file_name'] == sub_url.split('/')[-1].split('-')[0] + '.json')].any().all():
                                            writer.writerow(info)
                                    
                                self.fix(data_file)
        return self

if __name__ == "__main__":
    thething = Writting9GetLinks([num if isfloat(num) else int(num) for num in np.arange(9, 3.5, -0.5)]).get_urls(save=True, name='writing9', format='csv')    