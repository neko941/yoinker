import os
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class Scarper():
    def __init__(self, url, userAgent=None, pathUserAgent='./data/user_agent.txt'):
        self.url = url
        self.getUserAgents(pathUserAgent)
        if not userAgent:
            self.randomUserAgent()
        self.getSoup()

    def getUserAgents(self, pathUserAgent):
        self.userAgents = self.readTXT(os.path.abspath(pathUserAgent))

    def randomUserAgent(self):
        random.shuffle(self.userAgents)
        self.userAgent = self.userAgents[0].replace('\n','').strip()
        print(f"{self.userAgent = }")
        return self

    def getSoup(self):
        try:
            if not self.userAgent: self.randomUserAgent()
            self.response = requests.get(self.url, headers={"User-Agent": f"{self.userAgent}"})
            if self.response.status_code == 200:
                self.soup = BeautifulSoup(self.response.content, "html.parser")
            else:
                print(f'{self.response.status_code = }')
            return self
        except Exception as e:
            print(e)
            return

    def findText(self, name=None, id=None, class_=None, deleteChars=None, recursive=True, replaceChars=None):
        result = self.findAllText(name=name, class_=class_, id=id, recursive=recursive, limit=1, deleteChars=deleteChars, replaceChars=replaceChars)
        return result[0]
    
    def deleteCharacters(self, string, deleteChars):
        for d in deleteChars:
            string = string.replace(d, '')
        return string
    
    def replaceCharacters(self, string, replaceChars):
        for key, value in replaceChars.items(): 
            string = string.replace(key, value)
        return string

    def findAllText(self, limit=None, name=None, id=None, class_=None, deleteChars=None, recursive=True, replaceChars=None):
        result = self.soup.findAll(name=name, class_=class_, id=id, recursive=recursive, limit=limit)
        result = [r.get_text().strip() for r in result if r not in [None, '']]
        if deleteChars != None:
            if not isinstance(deleteChars, list):
                deleteChars = [deleteChars]
            result = [self.deleteCharacters(string=r, deleteChars=deleteChars) for r in result]
        if replaceChars != None:
            result = [self.replaceCharacters(string=r, replaceChars=replaceChars).strip() for r in result]
        return result

    def findAllHref(self, limit=None, name=None, id=None, class_=None, recursive=True):
        result = self.soup.findAll(name=name, class_=class_, id=id, recursive=recursive, limit=limit)   
        # print(result)
        urls = []
        urls.extend([r.get('href') for r in result])
        return urls

    def removeAll(self, limit=None, name=None, id=None, class_=None, recursive=True):
        for script in self.soup.findAll(name=name, class_=class_, id=id, recursive=recursive, limit=limit):
            script.decompose()
        return self

    def log(self, message, url, log_dir):
        if log_dir is None: return
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        with open(f'{os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d"))}.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now().strftime("%H:%M:%S")} - {url} - {message}\n')
    
    def fixTXT(self, path):
        uniqlines = set(open(path).readlines())
        bar = open(path, 'w').writelines(uniqlines)
        bar.close()

    def checkTXT(self, path):
        if not os.path.exists(path): 
            os.makedirs(os.path.dirname(path))
            with open(path, 'w') as fp:
                pass
    
    def readTXT(self, path):
        return [p.replace("\n", '').strip() for p in open(path, 'r').readlines()]
