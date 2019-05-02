from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from selenium import webdriver
import requests
import json
from bs4 import BeautifulSoup
from news_lib import *
from weather_lib import *
from getnews import *
from linebot.exceptions import InvalidSignatureError

from linebot.models import *
app= Flask(__name__)
line_bot_api = LineBotApi('xi3ziO6Yv6J2b4nz1vSLMMIRRTehz9VFkWpgzytaDNpKxhdnRbcGWzORpjZGUJd8cJ4StMvKZ4lYtn9ZYEi80ckyu0hcjdtq9+hFttTk/ztv0uKckGTaOGjbiCuxvY0zDJClw0Hf7Dj1ek11lsb6RgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a8acf3539e24e1b315f7be19ae0000bf')

# ngrok authtoken 7opmFdz4EXQnKC95w7Pvo_6XusjhM3F7Rwv66GFrvUr

@app.route('/')
def hello():
    return 'trivago'

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

    if event.message.text == "天氣":
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/ixEm52C.jpg',
                title='天氣',
                text='請選擇地區',
                actions=[
                    MessageTemplateAction(
                        label='台北天氣',
                        text='台北天氣',
                    ),
                    MessageTemplateAction(
                        label='台中天氣',
                        text='台中天氣'
                    ),
                    MessageTemplateAction(
                        label='台南天氣',
                        text='台南天氣'
                    ),
                    MessageTemplateAction(
                        label='高雄天氣',
                        text='高雄天氣'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    if event.message.text == "新聞":
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/ixEm52C.jpg',
                title='新聞',
                text='請選擇想搜尋的新聞社',
                actions=[
                    MessageTemplateAction(
                        label='聯合',
                        text='聯合',
                    ),
                    MessageTemplateAction(
                        label='自由',
                        text='自由'
                    ),
                    MessageTemplateAction(
                        label='中時',
                        text='中時'
                    ),
                    MessageTemplateAction(
                        label='tvbs',
                        text='tvbs'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    if "郵件" in event.message.text:
        aa = event.message.text
        href = aa.replace('郵件','')
        a = mail_news(href)
        if a != "":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="成功寄送，請前往信箱查看"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="寄送失敗，請檢查您的格式是否有問題"))
    
    if "搜尋" in event.message.text:
        aa = event.message.text
        aa = aa.replace(':','')
        aa = aa.replace(' ','')
        aa = aa.replace('[','')
        aa = aa.replace(']','')
        search = aa.replace('搜尋','')
        a = udn_search(search)
        cont1='\n'.join(a)
        
        b = free_search(search)
        cont2='\n'.join(b)
        
        c = tvbs_search(search)
        cont3='\n'.join(c)
        
        d = ct_search(search)
        cont4='\n'.join(d)
        content=cont1+'\n'+cont2+'\n'+cont3+'\n'+cont4
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
            

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

    elif event.message.text == "台中天氣" or event.message.text == "臺中天氣":
        a = Taichung_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "台北天氣" or event.message.text == "臺北天氣":
        a = Taipei_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "桃園天氣":
        a = Taoyuan_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "新竹天氣":
        a = Hsinchu_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "台南天氣" or event.message.text == "臺南天氣":
        a = Tainan_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "高雄天氣":
        a = Kaohsiung_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "台東天氣" or event.message.text == "臺東天氣":
        a = Taitung_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "花蓮天氣":
        a = Hualien_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "屏東天氣":
        a = Pingtung_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "回答我":
        a = "我盡力了"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "??":
        a="??"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "==":
        a="=="
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "^^":
        a="^^"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "早安":
        a = "早安安"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "找飯店":
        a = "trivago"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    else:
        a = "我是SheepYeeee，是個聊天機器人，如果你想看最新新聞，請輸入[新聞]，我會告訴你最新的即時新聞，如果你想搜尋新聞，請輸入[搜尋關鍵字]，如[搜尋天氣]、[搜尋櫻花]；如果你想知道今日天氣，請輸入[天氣]，或是[台中天氣]、[花蓮天氣]。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)




# message = TextSendMessage(text=event.message.text)
# line_bot_api.reply_message(event.reply_token,message)

