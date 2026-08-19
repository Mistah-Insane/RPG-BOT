import os
import socket
import time
from threading import Thread
from flask import Flask

# 1. Web server for Render Free Web Service
app = Flask(__name__)

@app.route('/')
def home():
    return "Twitch Bot is Live!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web_server, daemon=True).start()

# 2. Twitch IRC Bot
server = 'irc.chat.twitch.tv'
port = 6667

oauth = os.getenv('TWITCH_OAUTH')
nickname = os.getenv('TWITCH_NICKNAME', 'mistah_insane')
channel = os.getenv('TWITCH_CHANNEL', '#cyri97')
message = os.getenv('TWITCH_MESSAGE', '$rpg boss event')

if not oauth:
    raise ValueError("Missing TWITCH_OAUTH environment variable! Please add it in Render settings.")

s = socket.socket()
s.connect((server, port))
s.send(f"PASS {oauth}\r\n".encode('utf-8'))
s.send(f"NICK {nickname}\r\n".encode('utf-8'))
s.send(f"JOIN {channel}\r\n".encode('utf-8'))

while True:
    s.send(f"PRIVMSG {channel} :{message}\r\n".encode('utf-8'))
    time.sleep(60)
