import os
import socket
import time
from threading import Thread
from flask import Flask

# 1. Web server for Render Free Web Service
app = Flask(_name_)

@app.route('/')
def home():
    return "Twitch Bot is Live!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web_server, daemon=True).start()

# 2. Twitch IRC Bot Connection
server = 'irc.chat.twitch.tv'
port = 6667

oauth = os.getenv('TWITCH_OAUTH')
nickname = os.getenv('TWITCH_NICKNAME', 'mistah_insane')  # Set to mistah_insane
channel = os.getenv('TWITCH_CHANNEL', '#cyri97')

# Message 1: Sends every 60 seconds (1 minute)
message1 = os.getenv('TWITCH_MESSAGE_1', '$rpg boss event')
interval1 = 60 

# Message 2: Sends every 900 seconds (15 minutes)
message2 = os.getenv('TWITCH_MESSAGE_2', '$rpg boss battle')
interval2 = 900 

if not oauth:
    raise ValueError("Missing TWITCH_OAUTH environment variable! Please add it in Render settings.")

s = socket.socket()
s.connect((server, port))
s.send(f"PASS {oauth}\r\n".encode('utf-8'))
s.send(f"NICK {nickname}\r\n".encode('utf-8'))
s.send(f"JOIN {channel}\r\n".encode('utf-8'))

# Send initial messages on startup
s.send(f"PRIVMSG {channel} :{message1}\r\n".encode('utf-8'))
time.sleep(2)
s.send(f"PRIVMSG {channel} :{message2}\r\n".encode('utf-8'))

# Track last sent timestamps
last_sent_1 = time.time()
last_sent_2 = time.time()

# Main loop checking timers every second
while True:
    now = time.time()

    # Check timer for Message 1 ($rpg boss event)
    if now - last_sent_1 >= interval1:
        s.send(f"PRIVMSG {channel} :{message1}\r\n".encode('utf-8'))
        last_sent_1 = now
        time.sleep(1)

    # Check timer for Message 2 ($rpg boss battle)
    if now - last_sent_2 >= interval2:
        s.send(f"PRIVMSG {channel} :{message2}\r\n".encode('utf-8'))
        last_sent_2 = now
        time.sleep(1)

    time.sleep(1)
