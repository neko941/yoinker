import requests
from bs4 import BeautifulSoup 

class UserAgentStringScraper():
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        if self.response.status_code == 200:
            self.get_soup()

    def get_soup(self):
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def fetch(self):
        return [a.get_text() for a in self.soup.findAll(name='a') if 'Mozilla' in a.get_text()]

with open(r'user_agent.txt', 'w') as fp:
    for item in UserAgentStringScraper('https://useragentstring.com/pages/All/').fetch():
        fp.write("%s\n" % item)