from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YH8QSbOe6pJGB1C2+urMJupyk9Jnn80mwwjzO5t59L2I8BYG1jEBM5rU/JL5Vv+ZcJ4StMvKZ4lYtn9ZYEi80ckyu0hcjdtq9+hFttTk/zuaFz3OWKKA0ei5m/zI2fHC7ruIVlQnoYdsFAXa1Hi0HAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a8acf3539e24e1b315f7be19ae0000bf')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()