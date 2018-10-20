import os
import io
from PIL import Image

import settings
from vision import get_url_from_text

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    ImageMessage, MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(settings.YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNEL_SECRET)


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message_text(event):
    text_message = text_message.message.text
    if text_message.startswith("http"):
        send_text = get_url_from_text(text_message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=send_text))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="画像 または 画像のURLを送ってください！"))

@handler.add(MessageEvent, message=ImageMessage)
def handle_message_image(event):
    message_content = line_bot_api.get_message_content(message_id)
    img_bin = io.BytesIO(message_content)
    try:
        send_text = get_url_from_text(img_bin)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=send_text))
    except:
        print("Image---Error")
        
if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )