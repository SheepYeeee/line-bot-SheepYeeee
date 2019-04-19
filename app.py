from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import random

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
# Channel Secret
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#新聞
def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = []
    for index, data in enumerate(soup.select('div.item a')):
        if index == 20:           
            return content
    
        title = data.find('img')['alt']
        link =  data['href']
        link2 = 'https:'+ data.find('img')['data-src']
        content.append(title)
        content.append(link)
        content.append(link2)
        print("data：")
        print(content)   
    return content

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    msg = msg.encode('utf-8')
    if event.message.text == "你是誰":
        a="我是SheepYeeee"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
    elif event.message.text == "蘋果新聞":
        a=apple_news()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
    else: 
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)
    



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
