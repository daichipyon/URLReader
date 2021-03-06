import os
import io
from PIL import Image

import settings
from vision import get_url_from_text_gg

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    ImageMessage, MessageEvent, TextMessage, TextSendMessage, FollowEvent
)

app = Flask(__name__)

line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)

def send_message(message,event):
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=message))


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

@handler.add(FollowEvent)
def handle_message_followed(event):
    print("followed")
    message_followed = "フォローありがとうございます！　ここでは画像内のURLを読み込んで返します\n\n画像か画像のURLを送ってください!\n問題があればこちらに問い合わせください\n→Twitter:@ichida_guchiya"
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=message_followed))

@handler.add(MessageEvent, message=TextMessage)
def handle_message_text(event):
    text_message = event.message.text
    if text_message.startswith("http"):
        send_text = get_url_from_text_gg(image_url=text_message)
        print("send_text", send_text)
        send_message(send_text, event)
    else:
        send_message("画像 または 画像のURLを送ってください！", event)

@handler.add(MessageEvent, message=ImageMessage)
def handle_message_image(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    img_bin = (message_content.content)
    try:
        send_text = get_url_from_text_gg(image=img_bin)
        send_message(send_text, event)
    except:
        error_message = "URLを見つけることを出来ませんでした"
        send_message(error_message, event)


        
if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )