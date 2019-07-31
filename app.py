# SDK(software development kit): 使用官方釋出的SDK
# 通常web app的主要程式都取名叫app.py -> 程式放在網路上
# 架設伺服器的應用程式: flask, django
# Line Develop上webhooks要enabled，並輸入網址

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
# 要有以下2個code: token, secret才能操作這個程式
line_bot_api = LineBotApi('Zxj5kIZrk0v37Wj3V93O9kW1CEmoYiJAKcCvDSzRL6ItNzBOp0UfS8MDwMN23IqENWtW2DrHkzwz7oLRTVgMpsRb3T5bCHgjlpveEnpNQ1PqAyDJ6L136EaDjfWOBzLDlxsc+FKzNwmw32YqECcfUgdB04t89/1O/w1cDnyilFU=') # YOUR_CHANNEL_ACCESS_TOKEN
handler = WebhookHandler('bd1e309160e6d0827cb00da627b3943a') # YOUR_CHANNEL_SECRET

# 接收line傳來的訊息轉載到我們設定的伺服器的程式碼
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature) # 會觸發下面handle的程式碼去回覆訊息
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
# 以上都不用改
# 回覆訊息的程式碼，需要token
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# 檔案直接被執行才會執行程式
if __name__ == "__main__":
    app.run()