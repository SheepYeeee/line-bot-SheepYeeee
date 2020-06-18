# line-bot-SheepYeeee
###### tags: `chatbot`

<style>

h5{
color:red;
}
b{
color:red;
}
</style>

line robot 聊天機器人 基礎入門篇
===
紀錄一下line bot開發過程，目前機器人擁有的功能如下
- 觀看即時新聞，輸入"<b>聯合</b>"、"<b>自由</b>"、"<b>tvbs</b>"、"<b>中時</b>"
- 搜尋新聞，輸入搜尋+關鍵字，如"<b>搜尋大選</b>"、"<b>搜尋梅雨</b>"
- 郵寄新聞到個人信箱，輸入郵寄+新聞網址，如"<b>郵寄https://udn.com/news/story/6811/3796245</b>"，目前只能郵寄聯合、自由、tvbs、中時這四間新聞社的新聞。郵寄畫面如下:![](https://i.imgur.com/xKfBmvD.png)
- 填寫個人信箱，請先輸入"<b>我的資料</b>"做個人資料查驗，若信箱為空或是想更新信箱，請輸入更新信箱+個人郵件，如"<b>更新信箱abc123@gmail.com</b>"
- 查詢天氣，請輸入"<b>天氣</b>"，選擇欲搜尋的地區；亦可直接輸入"<b>台中天氣</b>、"<b>花蓮天氣</b>"
- 我的linebot的QRcode如下(目前透過ngrok架設，只有我開的時候能使用):
![](https://i.imgur.com/fNlRnxY.png)

---

## 1.去line developers註冊開發者
- 去[line developers](https://developers.line.me/en/)以本人帳號登入後，選擇創建Messaging API Account
- 跟著流程走，創建成功後去將 Use Webhook 改成enabled， Auto-reply messagese 改成disabled

---
## 2-1. 要上傳的檔案如下，先把這些檔案準備起來
- 主要的程式碼如下，等等要教如何檔案上傳至heroku(一種平台即服務PaaS，開發者可以在開發&部屬各種網站，支持多種語言)，或是透過ngrok(轉發伺服器，將外界的請求轉發到你本機指定的port)開放指定port請求。兩者擇一即可
-- 補充一點，line bot的webhook一定要是https開頭，上面兩種方法都有提供https服務
  - [app.py](#)
```python=
from flask import Flask,request,abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Channel access token (long-lived)')
# Channel Secret
handler = WebhookHandler('Channel secret ')

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
```

  - requirements.txt
  > line-bot-sdk
    flask
  - runtime.txt
  > python-3.7.0

  - Procfile
  > web: python app.py
  
  檔案資料夾會像這樣
  ![](https://i.imgur.com/ZilgRYa.png)


---
## 2-2.去註冊並安裝heroku，並試著將程式push上去
- [可以參考這篇文章](https://github.com/twtrubiks/Deploying-Flask-To-Heroku)
- 先完成 註冊 下載 安裝 這些步驟，才開始做push程式碼的動作

將code push上heroku常用的幾個cmd指令如下

> heroku login
> git init (只有第一次需要用)
> 
heroku app有兩種新建方式，前者是在cmd輸入heroku create，後者是在個人的heroku頁面新增，有app後才能繼續執行下面
> heroku git:remote -a 你的app名稱 
> #用 git 將資料夾與 heroku 連接

最後做push動作

> git add .
> git commit -m "first push"
> git push heroku master



---
## 2-3.去註冊並安裝ngrok，讓外網可以連線到本地端
- 先去ngrok的官網註冊並下載，在官網註冊完的同時會看到下圖畫面，紅框部分(紅框部分是為了連結剛才所註冊的ngrok帳戶)記得要存起來
  ![](https://i.imgur.com/NPye41Z.png)
- 程式檔準備好之後，在VScode執行app.py，執行畫面如下
  ![](https://i.imgur.com/TqaJbbn.png)
- 在打開剛才下載的ngrok.exe檔，將剛才說的紅框部分貼上並執行
- 再輸入 ngrok http 5000(這邊的port要跟app.py設定的port一樣)
- 成功執行畫面如下，紅線部分就是等等要貼上webhook的網址(若沒有執行上一步驟的話，ngrok會在執行時開始倒數八小時，也就是每八小時要重開一次)
 ![](https://i.imgur.com/xQOcVOF.png)


---
## 3.去更改webhook url

linebot-sheepyeeee-news是我的app在heroku的名稱，正確格式如下
> {HEROKU_APP_NAME}.herokuapp.com/callback
> 或是
> {???}.ngrok.io/callback

![](https://i.imgur.com/NUZZFuB.png)

更改完畢後記得按Verify，去測試有沒有正常回應，如果有出現像是
> <h5>webhook The webhook returned an invalid HTTP status code.</h5>
的提示，heroku部屬的就要去heroku查看View logs(類似執行日記)找bug；ngrok部屬的就去vscode的執行畫面看是哪個部分出問題

---
## 4.基本上完成以上步驟完成後 你的機器人就會跟你說話了

![](https://i.imgur.com/1fSF5vT.png)
 
接下來就可以針對你想賦予機器人什麼功能去寫code了─=≡Σ((( つ•̀ω•́)つ

[實際操作影片2019/04/22](https://drive.google.com/file/d/139dfgbhRQRtVXIIHCDqOQDjbKH1f1imW/view?usp=sharing)
[實際操作影片2019/05/03](https://drive.google.com/file/d/1pRDKPvutzXJ_mgn4lVWs81bI_t5HAcQ_/view?usp=sharing)
