import os
import csv
import json
import time
import requests
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

from utils import isfloat
from utils import find_all
from utils import advanced_split
from utils import isfloatfromstring
from utils import advanced_path_join

class Writing9Scraper():
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        if self.response.status_code == 200:
            self.get_soup()
        self.bug = 0

    def get_soup(self):
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def get_question(self):
        try:
            self.question = self.soup.find(name='h1', class_='jsx-3594441866').get_text().replace('\r\n', '').strip()
            return self.question
        except:
            self.bug = 1
            self.log('Question')

    def get_topics(self):
        try:
            self.topics = [topic.replace('#', '') for topic in self.soup.find(name='div', class_='jsx-2818493600 page-text__topics').get_text().strip().split(" ")]
            return self.topics
        except:
            self.bug = 1
            self.log('Topics')

    def get_submitter(self):
        try:
            self.submitter = self.soup.find(name='div', class_='jsx-2818493600 create-date').find('span', class_='jsx-2818493600').get_text().replace('Submitted by', '').replace('on', '').strip()
            return self.submitter
        except:
            self.submitter = ''

    def get_datetime(self):
        try:
            self.datetime = self.soup.find(name='time', class_='jsx-2818493600').get('datetime')
            return self.datetime
        except:
            self.bug = 1
            self.log('Datetime')

    def get_linking_words(self):
        try:
            self.linking_words = {
                'num_linking_words' : self.soup.find(name='div', class_='jsx-3229629309 highlight-legends__item highlight-legends__item_linkingwords').find(name='span', class_='jsx-3229629309 highlight-legends__item-counter').get_text(),
                'list_linking_words' : list(set([i.get_text().lower() for i in self.soup.findAll(name='span', class_='jsx-2885589388 linking-words') if i.get_text()!='']))
            }
            return self.linking_words
        except:
            self.bug = 1
            self.log('Linking Words')

    def get_repeated_words(self):
        try:
            rws = list(set([i.get_text().lower() for i in self.soup.findAll(name='span', class_='jsx-2310580937 repeated-word') if i.get_text()!='']))
            if not hasattr(self, 'full_text'):
                self.get_text()
            indices = [list(find_all(self.full_text, rw)) for rw in rws]
            self.repeated_words = {
                'num_repeated_words' : self.soup.find(name='div', class_='jsx-3229629309 highlight-legends__item highlight-legends__item_repeatedwords').find(name='span', class_='jsx-3229629309 highlight-legends__item-counter').get_text(),
                'list_repeated_words' : [{'word' : a, 'occurrences' : [{'start_idx' : c, 'end_idx' : c+len(a)} for c in b]} for a,b in zip(rws, indices)]
            }
            return self.repeated_words
        except:
            self.bug = 1
            self.log('Repeated Words')

    def get_text(self):
        try:
            for script in self.soup.findAll('div', class_='jsx-1879403401 hover'):
                script.decompose()

            self.text = advanced_split(
                text=self.soup.find('span', class_='jsx-242105113').get_text().strip(), 
                delimiters=['\r\n\r\n', '\n\n', '\n'])  

            self.full_text = " ".join(self.text)
            self.get_soup()
            return self.text
        except:
            self.bug = 1
            self.log('Text')


    def get_errors(self):
        try:
            self.errors = []
            for error in self.soup.findAll(name='span', class_='jsx-836047043 error'):
                
                error_word = error.find(name='span', class_='jsx-1879403401 text').get_text()
                
                previous_elements = []
                previous_element = error.previous_sibling
                if not previous_element == None:
                    while True:
                        previous_elements.insert(0, previous_element)
                        previous_element = previous_element.previous_sibling
                        if previous_element == None:
                            break
                previous = ''
                if len(previous_elements) != 0:
                    for ele in previous_elements:
                        if isinstance(ele, str):
                            previous += ele
                        else:
                            for script in ele.findAll(name='div', class_='jsx-1879403401 hover'):
                                script.decompose() 
                            previous += ele.get_text()
                # previous = ' '.join(previous.split('\r\n\r\n')).replace('\xa0', ' ')
                previous = advanced_split(text=previous, delimiters=['\r\n\r\n', '\n\n', '\n'], join_char=' ').replace('\xa0', ' ')
                
                try:
                    error_title = error.find('div', class_='jsx-1879403401 title').get_text().replace('\xa0', ' ')
                except:
                    error_title = ''

                try:
                    error_des = error.find('p', class_='jsx-1879403401 info').get_text().replace('\xa0', ' ').replace('show examples', '').replace('don\u2019t', 'do not').strip()
                except:
                    error_des = ''
                
                try:
                    suggetions = [j.get_text().strip() for j in error.find('div', class_='jsx-1879403401 suggestions').findAll('div', class_='jsx-1879403401 suggestion')]
                except:
                    suggetions = []
                self.errors.append({
                    'word' : error_word,
                    'start_idx' : len(previous),
                    'end_idx' : len(previous)+len(error_word),
                    'error' : error_title,
                    'error_des': error_des,
                    'suggetions': suggetions
                })
            
            self.errors = {
                'num_error' : self.soup.find(name='div', class_='jsx-3229629309 highlight-legends__item highlight-legends__item_mistake').find(name='span', class_='jsx-3229629309 highlight-legends__item-counter').get_text(),
                'error_list' : self.errors}
            return self.errors
        except:
            self.bug = 1
            self.log('Errors')

    def get_text_stats(self):
        try:
            stats = [int(stat.get_text()) for stat in self.soup.find(name='div', class_='jsx-2802957637 page-draft-text-analyzer__section-container page-draft-text-analyzer__stats').findAll(name='span', class_='jsx-2802957637')]
            self.num_paragraphs, self.num_words = stats
        except:
            self.bug = 1
            self.log('Text Statistics')
  
    def get_scores(self):
        try:
            self.scores = {'overall_band_score' : 0}
            for m in self.soup.findAll(name='div', class_='jsx-2802957637 page-draft-text-analyzer__section-container'):
                if 'Overall Band Score' in m.get_text():
                    self.scores['overall_band_score'] = float(m.get_text().replace('Overall Band Score', ''))
                else:
                    score = m.find(name='h3', class_='jsx-2802957637 page-draft-text-analyzer__section').get_text().split(':')
                    self.scores['_'.join(score[0].strip().lower().split(' '))] = ({
                        'overall_score' : float(score[1].strip())
                    })
                    for n in m.findAll(name='div', class_='jsx-2802957637 page-draft-text-analyzer__row'):
                        if isfloatfromstring(n.get_text()[:3]):
                            self.scores['_'.join(score[0].strip().lower().split(' '))]['_'.join(n.get_text()[3:].lower().split(' '))] = float(n.get_text()[:3])
                        elif n.get_text()[0].isdigit():
                            self.scores['_'.join(score[0].strip().lower().split(' '))]['_'.join(n.get_text()[1:].lower().split(' '))] = float(n.get_text()[0])
                        else:
                            self.scores['_'.join(score[0].strip().lower().split(' '))]['_'.join(n.get_text().lower().split(' '))] = 0.0       
        except:
            self.bug = 1
            self.log('Scores') 
        
    def log(self, message, log_dir='error_log'):
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        with open(f'{os.path.join(log_dir, datetime.now().strftime("%y-%m-%d"))}.txt', 'a') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} - {self.url} - {message}\n')
        
    def get_all_info(self, save_dir):
            time.sleep(1)
            if self.response.status_code == 200:
                print(f'Fetching => {self.url}')
                try:
                    self.get_text()
                    self.get_question()
                    self.get_topics()
                    self.get_submitter()
                    self.get_datetime()
                    self.get_linking_words()
                    self.get_repeated_words()
                    self.get_errors()
                    self.get_text_stats()
                    self.get_scores()   

                    data = {
                        'url' : self.url,
                        'file' : save_dir,
                        'topics' : self.topics,
                        'question' : self.question,
                        'scores' : self.scores,
                        'text' : self.text,
                        'errors' : self.errors,
                        'submitter' : self.submitter,
                        'num_words' : self.num_words,
                        'num_paragraphs' : self.num_paragraphs,
                        'linking_words' : self.linking_words,
                        'repeated_words' : self.repeated_words,
                        'datetime_submitted' : self.datetime
                    }

                    if self.bug == 0:
                        with open(advanced_path_join(save_dir), 'w') as fp:
                            json.dump(data, fp, indent=4, sort_keys=False) 
                        print(f'Data written => {advanced_path_join(save_dir)}', end='\n\n')
                    else:
                        print(f'Errors => {self.url}', end='\n\n') 
                except:
                    print(f'Errors => {self.url}', end='\n\n') 

if __name__ == "__main__":
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    for n in [num if isfloat(num) else int(num) for num in np.arange(9, 3.5, -0.5)]:
        if not os.path.exists(os.path.join(data_dir, os.path.join(str(n).replace('.', '')))):
            os.mkdir(os.path.join(data_dir, os.path.join(str(n).replace('.', ''))))

    with open('writing9.csv', newline='') as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            print(f'Count: {idx}')
            if row == ['url', 'band', 'file_name']:
                continue

            file_path = [data_dir, row[1], row[2]]
            if not os.path.exists(advanced_path_join(file_path)):
                Writing9Scraper(url=row[0]).get_all_info(save_dir=file_path)
            else:
                print(f'File exists => {advanced_path_join(file_path)}', end='\n\n')