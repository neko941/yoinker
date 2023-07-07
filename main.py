from yoinker.thanhnien_vn import ThanhNien_VN
from bs4 import BeautifulSoup
import requests
import time

def getThanhNien(path=None, id=None, mode='inc', overwrite=True, sleep=3):
    if path is not None:
        uniqlines = list(set([l.replace('\n', '') for l in open(path).readlines()]))
        uniqlines.sort(key=lambda x: int(x.split('post')[-1].replace('.html', '')))
        for line in uniqlines:
            ThanhNien_VN(
                url=line.replace('\n','').strip(),
                downloadedDataPath='./data/thanhnien_vn/urls.txt',
                pathUserAgent='./data/user_agent.txt',
                error_log='./data/thanhnien_vn/log',
                savePath='./data/thanhnien_vn').execute(overwrite=overwrite, skipTopics=['Video'])
            for i in range(sleep):
                print(f'Sleeping: {i+1}/{sleep}')
                time.sleep(1)
    
    if id is not None:
        id = int(id)
        while True:
            ThanhNien_VN(
                id=id,
                downloadedDataPath='./data/thanhnien_vn/urls.txt',
                pathUserAgent='./data/user_agent.txt',
                error_log='./data/thanhnien_vn/log',
                savePath='./data/thanhnien_vn').execute(overwrite=overwrite, skipTopics=['Video'])
            if mode == 'inc': id += 1
            if mode == 'dec': id -= 1
            for i in range(sleep):
                print(f'Sleeping: {i+1}/{sleep}')
                time.sleep(1)

if __name__ == '__main__':
    # getThanhNien(path='url/thanhnien.txt', overwrite=False)

    start = 1405280  # 1495397 
    # end = 1520475
    end = 1520958
    # getThanhNien(id=end+1, overwrite=True, mode='inc')
    getThanhNien(id=start+1, overwrite=True, mode='dec')

    # getThanhNien(id=1520475)
    
    # ThanhNien_VN(
    #     url='https://thanhnien.vn/chay-ve-may-bay-dip-le-30-4-xe-khach-cam-chung-post1452592.html',
    #     downloadedDataPath='./data/thanhnien_vn/urls.txt',
    #     pathUserAgent='./data/user_agent.txt',
    #     error_log='./data/thanhnien_vn/log',
    #     savePath='./data/thanhnien_vn').getTopic()

    # ThanhNien_VN(
    #     id=1520475,
    #     downloadedDataPath='./data/thanhnien_vn/urls.txt',
    #     pathUserAgent='./data/user_agent.txt',
    #     error_log='./data/thanhnien_vn/log',
    #     savePath='./data/thanhnien_vn').execute(overwrite=True)

    # id = 1520475
    # response = requests.get(
    #     url=f"https://www.google.com/search?q=allinurl%3Apost{id}", 
    #     headers={"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Iron/0.2.152.0 Safari/12079480.525"},)
    # # print(response.status_code)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.content, "html.parser")
    # result = soup.findAll(name='a', href=True)
    # result = [r['href'] for r in result if 'thanhnien.vn' in r['href']]
    # url = result[0].replace('/url?q=', '').split('.html')[0] + '.html'
    # print(url)