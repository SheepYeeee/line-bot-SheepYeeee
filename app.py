from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
import requests
import json
from bs4 import BeautifulSoup

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
app= Flask(__name__)
line_bot_api = LineBotApi('xi3ziO6Yv6J2b4nz1vSLMMIRRTehz9VFkWpgzytaDNpKxhdnRbcGWzORpjZGUJd8cJ4StMvKZ4lYtn9ZYEi80ckyu0hcjdtq9+hFttTk/ztv0uKckGTaOGjbiCuxvY0zDJClw0Hf7Dj1ek11lsb6RgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a8acf3539e24e1b315f7be19ae0000bf')


@app.route('/')
def hello():
    return 'trivago'

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
        # https://www.chinatimes.com/realtimenews/20190422002410-260410?chdtv
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


@app.route('/callback',methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    if "搜尋" in event.message.text:
        aa = event.message.text
        aa = aa.replace(':','')
        aa = aa.replace(' ','')
        search = aa.replace('搜尋','')
        a = udn_search(search)
        cont1='\n'.join(a)
        
        b = free_search(search)
        cont2='\n'.join(b)
        
        c = tvbs_search(search)
        cont3='\n'.join(c)
        
        d = ct_search(search)
        cont4='\n'.join(d)
        
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cont1+'\n'+cont2+'\n'+cont3+'\n'+cont4))
            

    if event.message.text == "聯合":
        a = udn_news()
        content='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif event.message.text == "自由":
        a = free_news()
        content='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif event.message.text == "tvbs":
        a = tvbs_news()
        content='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif event.message.text == "中時":
        a = ct_news()
        content='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

    elif event.message.text == "你好":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    elif event.message.text == "你是誰":
        a = "我是SheepYeeee，是個聊天機器人，如果你想看最新新聞，請輸入[中時]、[tvbs]、[聯合]、[自由]，我會為你找出該新聞社最新的新聞，如果你想搜尋新聞，請輸入[搜尋關鍵字]，如[搜尋天氣]、[搜尋櫻花]。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "回答我":
        a = "我盡力了"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "早安":
        a = "早安安"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "找飯店":
        a = "trivago"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    else:
        a = "我是SheepYeeee，是個聊天機器人，如果你想看最新新聞，請輸入[中時]、[tvbs]、[聯合]、[自由]，我會為你找出該新聞社最新的新聞，如果你想搜尋新聞，請輸入[搜尋關鍵字]，如[搜尋天氣]、[搜尋櫻花]。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)




# message = TextSendMessage(text=event.message.text)
# line_bot_api.reply_message(event.reply_token,message)

