from flask import Flask, request, abort,make_response,jsonify
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
import pymysql
import re
import random




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

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResult(req):

    if req.get('queryResult').get('action') != "askweather":
        print("Please check your action name in DialogFlow...")
        return {}

    result = req.get("queryResult")
    parameters = result.get("parameters")
    citys = parameters.get('taiwan-city')
    city = "".join(citys)
    if city == "taichung":
        a = Taichung_City()
        b ='\n'.join(a)
        speech = b
    elif city == "taipei":
        a = Taipei_City()
        b ='\n'.join(a)
        speech = b
    elif city == "tainan":
        a = Tainan_City()
        b ='\n'.join(a)
        speech = b
    elif city == "kaohsiung":
        a = Kaohsiung_City()
        b ='\n'.join(a)
        speech = b
    elif city == "桃園":
        a = Taoyuan_City()
        b ='\n'.join(a)
        speech = b
    else:
        speech = "Hi," + city 
    print("Response:"+speech)
    my_result = {
                    "fulfillmentText": speech,
                    "source": "agent"
                }
    return my_result
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    db = pymysql.connect(host='localhost',user='root',password='0000',db='sheepyeeee_news',charset='utf8')
    cur = db.cursor()

    if event.message.text == "我的資料":
        your = event.source.user_id
        sql="INSERT INTO `user` (`id`) SELECT %s WHERE NOT EXISTS (SELECT `id` FROM `user` WHERE `id`=%s)"
        cur.execute(sql,(your,your))
        sqli = "SELECT * FROM `user` WHERE id = %s"
        cur.execute(sqli,(your))
        rows = cur.fetchall()
        db.commit()
        cur.close()
        for row in rows:
            mail = row[1]
            if mail is None:
                a = "你的id為["+your
                b = "信箱為空，請輸入您的的信箱，輸入格式如[更新信箱abc@gmail.com]"
                c = a+"]，"+b
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=c))
            else:
                a = "你的id為["+your
                b = "信箱為["+mail+"]，若要更新信箱，請輸入更新信箱+你的emai，輸入格式如[更新信箱abc@gmail.com]"
                c = a+"]，"+b
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=c))



    if "更新信箱" in event.message.text:
        user_id = event.source.user_id
        email = event.message.text.replace('更新信箱','')
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',email):
            sql = "UPDATE `user` SET email= %s Where id = %s"
            cur.execute(sql,(email,user_id))
            rows = cur.fetchall()
            reply = "更新成功"
            db.commit()
            cur.close()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
        else:
            reply="信箱格式錯誤，請重新輸入"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
        
        

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
                thumbnail_image_url='https://i.imgur.com/NuAGCfY.jpg',
                title='新聞',
                text='請選擇要看哪一種新聞',
                actions=[
                    MessageTemplateAction(
                        label='即時新聞',
                        text='即時新聞',
                    ),
                    MessageTemplateAction(
                        label='各家新聞',
                        text='各家新聞'
                    )
                
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    if event.message.text == "各家新聞":
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/NuAGCfY.jpg',
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

    if "郵寄" in event.message.text:
        aa = event.message.text
        href = aa.replace('郵寄','')
        your = event.source.user_id
        sql = "SELECT * FROM `user` WHERE id = %s"
        cur.execute(sql,(your))
        rows = cur.fetchall()
        
        for row in rows:
            mail = row[1]
            db.commit()
            cur.close()
        if mail is None or mail == " " or mail == "":
            reply = "您的信箱為空，請先查驗你的身分，請輸入[我的資料]"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        else:
            a = mail_news(href,mail)
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
    elif event.message.text == "即時新聞":
        def_list = [udn_news,tvbs_news,free_news,ct_news]
        a = random.choice(def_list)()
        content='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif event.message.text == "你好":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    elif  "台中天氣" in event.message.text or "臺中天氣" in event.message.text:
        a = Taichung_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "台北天氣" in event.message.text or "臺北天氣" in event.message.text:
        a = Taipei_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "基隆天氣" in event.message.text:
        a = Taipei_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "桃園天氣" in event.message.text:
        a = Taoyuan_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "新竹天氣" in event.message.text:
        a = Hsinchu_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "台南天氣" in event.message.text or "臺南天氣" in event.message.text:
        a = Tainan_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "高雄天氣" in event.message.text:
        a = Kaohsiung_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "新北天氣" in event.message.text:
        a = New_Taipei_City()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "台東天氣" in event.message.text or "臺東天氣" in event.message.text:
        a = Taitung_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "苗栗天氣" in event.message.text:
        a = Miaoli_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "彰化天氣" in event.message.text:
        a = Changhua_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "雲林天氣" in event.message.text:
        a = Yunlin_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "嘉義天氣" in event.message.text:
        a =Chiayi_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "宜蘭天氣" in event.message.text:
        a =Yilan_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "澎湖天氣" in event.message.text:
        a =Penghu_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "南投天氣" in event.message.text:
        a = Nantou_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "花蓮天氣" in event.message.text:
        a = Hualien_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif "屏東天氣" in event.message.text:
        a = Pingtung_County()
        b ='\n'.join(a)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "新聞功能":
        a = "我是SheepYeeee，是個聊天機器人，如果你想看最新新聞，請輸入[新聞]，我會告訴你最新的即時新聞，如果你想搜尋新聞，請輸入[搜尋關鍵字]，如[搜尋櫻花]；如果你想要將喜歡的新聞郵寄至個人信箱，請輸入[郵寄網址]，如[郵寄https: // example . com]，我會將新聞內容及原文連結郵寄到你的個人信箱，目前只有聯合、自由、tvbs、中時的新聞可以郵寄。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))
    elif event.message.text == "天氣功能":
        b = "如果你想知道今日天氣，請輸入[天氣]，或是[台中天氣]、[花蓮天氣]、[台南天氣]...等。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=b))
    elif event.message.text == "個人資料功能":
        c = "如果你不確定是否輸入了你的個人信箱，請先輸入[我的資料]查驗，若信箱為空或是想要換別的信箱，請輸入[更新信箱+個人信箱]，如[更新信箱abc@gmail.com]"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=c))
    else:
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/qNms29t.jpg',
                title='使用說明',
                text='請選擇想了解的服務',
                actions=[
                    MessageTemplateAction(
                        label='新聞功能',
                        text='新聞功能',
                    ),
                    MessageTemplateAction(
                        label='天氣功能',
                        text='天氣功能'
                    ),
                    MessageTemplateAction(
                        label='個人資料功能',
                        text='個人資料功能'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        


    # db.commit()
    # cur.close()




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)




# message = TextSendMessage(text=event.message.text)
# line_bot_api.reply_message(event.reply_token,message)

