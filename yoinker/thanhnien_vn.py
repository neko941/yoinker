from yoinker.utils.Yoinker import Scarper
from urlextract import URLExtract
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
import requests
import json
import os

def next_url(url):
    try:
        return [a.find(name='a').get('href') for a in BeautifulSoup(requests.get(url).content, "html.parser").find(name='div', class_='zone--timeline').find(name='nav', class_='pag').findAll(name='li')][-1]
    except:
        return None

class SkipTopicException(Exception):
    """Base class for other exceptions"""
    pass

class NoPostURL(Exception):
    print('NoPostURL')
    pass

class ThanhNien_VN(Scarper):
    def __init__(self, downloadedDataPath, url=None, id=None, userAgent=None, pathUserAgent='./data/user_agent.txt', error_log='./data/thanhnien_vn/log', numGoofleResults=10, savePath='./data/thanhnien_vn'):
        self.numGoofleResults = numGoofleResults

        assert(any([url is not None, id is not None]))
        self.id = id
        self.url = url
        if userAgent is None:
            self.getUserAgents(pathUserAgent) 
            self.randomUserAgent()
        else:
            self.userAgent = userAgent
        if self.url is None:
            self.getURL()
        if self.id is None:
            self.getID()
        print(f'{self.url = }')
        print(f'{self.id = }')
        Scarper.__init__(self, url=self.url, userAgent=self.userAgent, pathUserAgent=Path(pathUserAgent))
        self.error_log = error_log
        
        self.savePath = Path(savePath)
        self.downloadedDataPath = downloadedDataPath
        self.downloadedData = None
        self.sub_urls = []
        self.bug = 0

    def getURL(self):
        # for url in search(
        #                     term=f'allinurl:post{self.id}', 
        #                     num_results=self.numGoofleResults, 
        #                     lang="en"):
        #     if 'https://thanhnien.vn' in url:
        #         self.url = url
        #         return self
        response = requests.get(
            url=f"https://www.google.com/search?q=allinurl%3Apost{self.id}", 
            headers={"User-Agent": f"{self.userAgent}"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
        try:
            result = soup.findAll(name='a', href=True)
            result = [r['href'] for r in result if 'thanhnien.vn' in r['href']]
            if len(result) < 1: raise NoPostURL
            self.url = 'https://thanhnien' + result[0].split('https://thanhnien')[1]
            self.url = self.url.split('.html')[0] + '.html'
            return self
        except:
            return
            
    def get_sub_urls(self):
        self.randomUserAgent()
        self.get_soup(self.url)
        sub_urls = self.findAllHref(name="a", class_="story__thumb")
        sub_urls = [urljoin(self.url, su) for su in sub_urls]
        return sub_urls

    def getID(self):
        self.id = int(self.url.split('post')[-1].replace('.html', ''))
        return self

    def fixTXT(self):
        uniqlines = list(set([l.replace('\n', '') for l in open(self.downloadedDataPath).readlines()]))
        uniqlines.sort(key=lambda x: int(x.split('post')[-1].replace('.html', '')))
        uniqlines = [f"{l}\n" for l in uniqlines]
        open(self.downloadedDataPath, 'w').writelines(uniqlines)
        return self

    def getDownloadedData(self):
        log = self.downloadedDataPath
        self.checkTXT(log)
        self.downloadedData = self.readTXT(log)
        return self
    
    def getTitle(self):
        try:
            self.title = self.findText(name='h1', class_="details__headline cms-title")
        except:
            try:
                self.title = self.findText(name='h2', class_="title cms-title")
            except:
                self.bug = 1
                self.log('Title', self.url, self.error_log)
        
        return self
    
    def getAuthor(self):
        try:
            self.author = self.soup.find(name='div', class_="details__author").find(name='div', class_='details__author__meta').find(name='a').get('title')
        except:
            try:
                self.author = self.findText(name='span', class_="author")
            except:
                self.bug = 1
                self.log('Author', self.url, self.error_log)
        return self

    def getDateTime(self):
        try:
            self.datetime =  self.soup.find(name='div', class_="meta").find(name='time').get('datetime')
            self.year = self.datetime[:4]
            self.month = self.datetime[5:7]
            print(f'{self.datetime = }')
        except:
            self.bug = 1
            self.log('Datetime', self.url, self.error_log)
        return self
    
    def getAbstract(self):
        try:
            self.abstract =  self.soup.find(id='chapeau').get_text().strip()
        except:
            self.bug = 1
            self.log('Abstract', self.url, self.error_log)
        return self
    
    def getTopic(self):
        try:
            self.topic = [t.get_text() for t in self.soup.find(name='div', class_='breadcrumb-detail').findAll(name='li', class_='breadcrumb-item') if t.get_text() != '']
        except:
            try:
                self.topic = [self.findText(name='div', class_='category')]
            except:
                self.topic = []
                self.bug = 1
                self.log('Topic', self.url, self.error_log)
        
        return self

    def getTags(self):
        try:
            self.tags = [a.get('title').strip() if a.get('title').strip().isupper() else a.get('title').strip().title() for a in self.soup.find(id='abde').find(name='div', class_='details__tags').findAll(name='a')]
        except:
            try:
                self.tags = [a.get_text().strip() if a.get_text().strip().isupper() else a.get_text().strip().title() for a in self.soup.find(name='ul', class_='list list-keyword').findAll(name='li', class_='item')]
            except:
                self.tags = []
                self.log('Tags', self.url, self.error_log)
        return self

    def getContent(self):
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
            self.log('Content', self.url, self.error_log)
        return self

    def getMedia(self):
        self.media = []
        count = 1
        try:
            for ele in self.soup.findAll(name='table', class_='video'):
                try:
                    caption = ele.find(class_='caption').get_text().strip().replace('Ảnh chụp từ clip', '')
                except:
                    caption = ''
                urls = str(ele.find(name='script'))
                urls = urls.replace("'", ' ').replace('"', ' ')
                extractor = URLExtract()
                urls = extractor.find_urls(urls)
                urls = [url for url in urls for e in ['mp4', 'mkv'] if url.endswith(e)]
                extenstion = urls[0].split('.')[-1]

                medium = {
                    "file" : f'{self.id}_{count}.{extenstion}',
                    "url" : urls[0],
                    "id" : '',
                    "sorce" : '',
                    "caption" : caption
                }
                ele.decompose()
                self.media.append(medium)
                count += 1

            for ele in self.soup.findAll(name='table', class_='picture'):
                if ele.find(name='img') is None: continue
                if ele.find(name='img').has_attr('data-src'):
                    url = ele.find(name='img')['data-src']
                else:
                    url = ele.find(name='img')['src']
                extenstion = url.split('.')[-1]
                try:
                    source = ele.find(class_='source').get_text().strip()
                    ele.find(class_='source').decompose()
                except:
                    source = ''
                
                try:
                    id = ele.find(name='img')['data-image-id']
                except:
                    id = ''

                try:
                    caption = ele.find(class_='caption').get_text().strip()
                except:
                    caption = ''
                medium = {
                    "file" : f'{self.id}_{count}.{extenstion}',
                    "url" : url,
                    "id" : id,
                    "sorce" : source,
                    "caption" : caption
                }
                ele.decompose()
                self.media.append(medium)
                count += 1
            
            # try:
            #     ele = self.soup.find(name='figure', class_='image')
            #     url = ele.find(name='img')['src']
            #     caption = ele.find(name='img')['alt']
            #     medium = {
            #         "file" : f'{self.id}_{count}.{extenstion}',
            #         "url" : url,
            #         "id" : id,
            #         "sorce" : source,
            #         "caption" : caption
            #     }
        except:
            self.bug = 1
            self.log('Meida', self.url, self.error_log)

    def isExist(self):
        if self.downloadedData is None: self.getDownloadedData()
        if self.url in self.downloadedData:
            return True
        else:
            return False

    def execute(self, overwrite=False, skipTopics=None, skipVideo=True):
        if self.downloadedData is None: self.getDownloadedData()
        if self.url is None: 
            print(f'Found no URL with ID {self.id}', end='\n\n\n\n\n')
            self.log('URL', self.id, self.error_log)
            return
        if not overwrite:
            if self.isExist(): 
                print(f'Exist ==> {self.url}', end='\n\n\n\n\n')
                return
        self.getTopic()
        try:
            if skipTopics is not None:
                if not isinstance(skipTopics, list):
                    skipTopics = [skipTopics]
                for t in skipTopics:
                    if t in self.topic:
                        print(f'Skip Topic: {self.topic}', end='\n\n\n\n')
                        raise SkipTopicException
        except SkipTopicException:
            return
        
        self.getTitle()
        self.getAuthor()
        self.getDateTime()
        self.getAbstract()
        self.getTags()
        self.getMedia()
        self.getContent()
        # self.getSoup()
        if self.bug == 0:
            # update the log for not downloading the article twice
            open(os.path.abspath(self.downloadedDataPath), 'a', encoding='utf-8').write(f'{self.url}\n')
            self.fixTXT()

            # make directory if it doesn't exist
            os.makedirs(os.path.join(self.savePath, self.year, self.month, str(self.id)), exist_ok=True)
            # get file name based on the url
            data_file = os.path.join(self.savePath, self.year, self.month, str(self.id), f'{self.id}.json')
            # format the data into json format
            data = {
                'id' : self.id,
                'topic' : self.topic,
                'url' : self.url,
                'title' : self.title,
                'datetime' : self.datetime,
                'author' : self.author,
                'abstract' : self.abstract,
                'content' : self.content,
                'tags' : self.tags,
                'media' :self.media
            }
            # write down the data
            with open(data_file, 'w', encoding='utf8') as fp:
                json.dump(data, fp, indent=4, sort_keys=False, ensure_ascii=False) 
            # display the results
            print(f'Data written => {data_file}')
            # try:
            for medium in self.media:
                if skipVideo and any([r in medium['file'] for r in ['mp4', 'mkv']]): continue
                try:
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', self.userAgent)]
                    urllib.request.install_opener(opener)
                    path = os.path.join(self.savePath, self.year, self.month, str(self.id), medium['file'])
                    print(f"Retrieving ==> {medium['url']}")
                    urllib.request.urlretrieve(medium['url'], path)
                    print(f'Save       ==> {path}')
                except:
                    if os.path.exists(path): os.remove(path)
                    self.log('Media', medium['url'], self.error_log)
                    self.log('Media', self.url, self.error_log)
            print('\n\n')
        else:
            print(f"Error ==> {self.url}", end='\n\n')
        print('\n\n\n') 