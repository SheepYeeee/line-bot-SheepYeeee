import requests
import json
from bs4 import BeautifulSoup

#tvbs
def tvbs_news():
    url = f'https://news.tvbs.com.tw/realtime'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    lists = soup.find('ul', attrs={'id':'realtime_data'})
    rows=lists.find_all('li')

    content=[]
    i=0
    for row in rows:
        link=row.find_next('a')#新聞連結
        thisurl = link.get('href')
        thisurl='https://news.tvbs.com.tw/'+thisurl
        titles=link.find_next('h2')#新聞標題
        time = titles.find_next('div',attrs={'class':'icon_time time'})

        if i<=9:
                content.append(time.text)
                content.append(titles.text)
                content.append(thisurl)
        i+=1
    return content

#聯合
def udn_news():
    url = f'https://udn.com/news/index'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    rowsss = soup.find('div', attrs={'class':'tabs_box_wrapper'})
    tab=rowsss.find_next('div',attrs={'id':'tab1'})
    dl=tab.find_next('dl')
    rows=dl.find_all('dt')
    content=[]

    for row in rows:
        title=row.find_next('a')#新聞連結
        thisurl=title.get('href')
        content.append(title.text)
        content.append(thisurl)
    return content
#自由時報
def free_news():
    url = f'https://news.ltn.com.tw/list/breakingnews/all'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    lists = soup.find('ul', attrs={'class':'list'})
    rows=lists.find_all('a',attrs={'class':'tit'})

    content=[]
    i=0
    for row in rows:
        time=row.find_next('span')#發布時間
        titles=time.find_next('p')#新聞標題
        thisurl=row.get('href')
        thisurl='https:'+thisurl
        if i<=9:
                content.append(time.text)
                content.append(titles.text)
                content.append(thisurl)
        i+=1
    return content

#中時
def ct_news():
    url = f'https://www.chinatimes.com/realtimenews?chdtv'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    rows = soup.find_all('div', attrs={'class':'col'})
    content=[]
    i=0
    for row in rows:
        h3 = row.find_next('h3')#新聞連結
        link = h3.find_next('a')
        thisurl = link.get('href')
        thisurl = 'https://www.chinatimes.com'+thisurl+'?chdtv'

        time = link.find_next('time')#發布時間
        time = time.get('datetime')

        if i<=9:
                content.append(time)
                content.append(link.text)
                content.append(thisurl)
        i+=1
    return content


#搜尋聯合
def udn_search(keywords):
    url = f'https://udn.com/search/result/2/'+str(keywords)
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    items = soup.find('div', attrs={'id':'search_content'})
    rows = items.find_all('dt')
    content=[]
    i=0
    for row in rows:
        link=row.find_next('a')#新聞連結
        thisurl=link.get('href')
        title=link.find_next('h2')
        time=link.find_next('span')
        time=time.text.replace(' ','')
        time = time.split('：')
        if i<=2:
                content.append(time[1])
                content.append(title.text)
                content.append(thisurl)
        i+=1
    return content

#搜尋自由
def free_search(keywords):
    url = f'https://news.ltn.com.tw/search?keyword='+str(keywords)
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    lists = soup.find('ul', attrs={'id':'newslistul'})
    rows=lists.find_all('li')
    content=[]
    i=0
    for row in rows:
        time = row.find_next('span')#發布時間
        link = time.find_next('a')#新聞連結
        titles = link.find_next('p')#新聞標題
        thisurl = link.get('href')
        thisurl='https://news.ltn.com.tw/'+thisurl
        if i<=2:
                content.append(time.text)
                content.append(titles.text)
                content.append(thisurl)
        i+=1
    return content


#搜尋tvbs
def tvbs_search(keywords):
    url = f'https://news.tvbs.com.tw/news/searchresult/news?search_text='+str(keywords)
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    lists = soup.find('div', attrs={'class':'search_list_div'})
    items = lists.find_next('ul')
    rows = items.find_all('li')
    content=[]
    i=0
    for row in rows:
        link=row.find_next('a')#新聞連結
        thisurl = link.get('href')
        titles = link.find_next('div',attrs={'class':'search_list_txt'})
        time = titles.find_next('div',attrs={'class':'icon_time'})
        if i<=2:
                content.append(time.text)
                content.append(titles.text)
                content.append(thisurl)
        i+=1
    return content


#搜尋中時
def ct_search(keywords):
    url = f'https://www.chinatimes.com/search/'+str(keywords) +'?chdtv'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    uls = soup.find('div', attrs={'class':'item-list'})
    rows = uls.find_all('li')
    content=[]
    i=0
    for row in rows:
        h3=row.find_next('h3',attrs={'class':'title'})#新聞連結
        link=h3.find_next('a')
        thisurl = link.get('href')
        # thisurl='https://www.chinatimes.com'+thisurl+'?chdtv'
        time=link.find_next('time')#發布時間
        time=time.get('datetime')
        if i<=1:
                content.append(time)
                content.append(link.text)
                content.append(thisurl)
        i+=1
    return content