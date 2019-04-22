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
    if event.message.text == "聯合":
        a = udn_news()
        content='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif event.message.text == "自由":
        a = free_news()
        content='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif event.message.text == "你好":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    elif event.message.text == "你是誰":
        a = "我是SheepYeeee，是個聊天機器人，如果你想看最新新聞，請輸入[聯合]、[自由]，我會為你找出該新聞社最新的新聞"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "回答我":
        a = "我盡力了"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "早安":
        a = "早安安"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "找飯店":
        a = "trivago\n"+"https://tc.trip.com/?Allianceid=742329&SID=1621595&ds_cid=71700000038520126&ds_kid=43700034994699689&utm_source=google&utm_medium=cpc&utm_campaign=GG_SE_TW_zh_Hotel_Competitor_NA_Exact%20TC&gclid=CjwKCAjwqfDlBRBDEiwAigXUaCmd5wlWyxr2oRKU0sJK1cc4WJin_OARz2pd30l0bdsWgUt-DMa7FRoCCMkQAvD_BwE&gclsrc=aw.ds"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)

