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
    def __init__(self):
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

    def get_urls(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            sub_urls = self.get_sub_urls(url)
        return sub_urls

# for i in range(100):
    # if len(Writting9GetLinks().get_sub_urls(f'https://writing9.com/band/9/{i}')) == 0:
    #     print(f'https://writing9.com/band/9/{i}')
print(Writting9GetLinks().get_sub_urls(f'https://writing9.com/band/9/18'))