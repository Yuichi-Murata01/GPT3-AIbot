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
import openai

openai.api_key = '*******************************'

app = Flask(__name__)

line_bot_api = LineBotApi(
    '*****************************')
handler = WebhookHandler('***********************')


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
    res = openai.Completion.create(
       engine="davinci",
       prompt=f"日本語AIチャットボット\n日本人の質問をAIが日本語で答えます\nHuman:{event.message.text}\nAI:",
       temperature=0.9,
       max_tokens=150,
       presence_penalty=0.6,
       stop=["\n", "Human:", "AI:"]
   )

   line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=res["choices"][0]["text"]))


if __name__ == "__main__":
   app.run()
