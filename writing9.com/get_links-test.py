import os
import csv
import time
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

from utils import isfloat
from utils import flatten_list

class Writting9GetLinks():
    def __init__(self, bands):
        self.bands = bands
        self.errors = []
        self.info = []
    
    def save_errors(self):
        with open('error_pages.txt', 'a') as f:
            f.write("\n".join(str(item) for item in self.errors))
        print(f'Total errors: {len(self.errors)}')

    def get_sub_urls(self, url):
        return flatten_list([[f"https://writing9.com{a.get('href')}" for a in item.find_all('a', href=True)] for item in BeautifulSoup(requests.get(url).content, "html.parser").findAll(name='div', class_='jsx-2609154510 item')])
    
    def fix(self, file_name):
        df = pd.read_csv(file_name, index_col=0)
        df.drop_duplicates(keep='first', ignore_index=True)
        df.to_csv(file_name)

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
                        self.errors.append(url)
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
                                    if data.shape[0] == 1:
                                        data = pd.concat([
                                            data, 
                                            pd.DataFrame([{
                                                'url' : sub_url, 
                                                'band' : str(band).replace('.', ''), 
                                                'file_name' : sub_url.split('/')[-1].split('-')[0] + '.json'
                                                }])
                                            ], axis=1)
                                    else:               
                                        if not data.loc[(data['url'] == sub_url) & (data['band'] == band) & (data['file_name'] == sub_url.split('/')[-1].split('-')[0] + '.json')].any().all():
                                            data = pd.concat([
                                                data, 
                                                pd.DataFrame({
                                                    'url' : sub_url, 
                                                    'band' : str(band).replace('.', ''), 
                                                    'file_name' : sub_url.split('/')[-1].split('-')[0] + '.json'
                                                    }, index=data.shape[0])
                                                ])
                                data.to_csv(data_file)
                                self.fix(data_file)
        return self

if __name__ == "__main__":
    thething = Writting9GetLinks([num if isfloat(num) else int(num) for num in np.arange(9, 3.5, -0.5)]).get_urls(save=True, name='writing9', format='csv')    
    thething.save_errors()