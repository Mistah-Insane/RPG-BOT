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

# 2. Twitch IRC Bot Connection
server = 'irc.chat.twitch.tv'
port = 6667

oauth = os.getenv('TWITCH_OAUTH')
nickname = os.getenv('TWITCH_NICKNAME', 'mistah_insane')  # Set to mistah_insane

# Target channels set directly as default values (added sugarqueenjanice)
default_channels = '#cyri97 #the_insane_arcade #viviladee #sugarqueenjanice'
raw_channels = os.getenv('TWITCH_CHANNEL', default_channels).split()
channels = [ch if ch.startswith('#') else f"#{ch}" for ch in raw_channels]

# Filter channel lists for specific messages
msg1_targets = [ch for ch in channels if ch in ['#cyri97', '#viviladee']]
msg2_targets = channels  # All channels (includes #sugarqueenjanice)

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

# Join all target channels
for channel in channels:
    s.send(f"JOIN {channel}\r\n".encode('utf-8'))

# Helper function to send messages to a specific list of channels
def send_to_channels(msg, target_channels):
    for channel in target_channels:
        s.send(f"PRIVMSG {channel} :{msg}\r\n".encode('utf-8'))
        time.sleep(0.5)  # Short pause to prevent rate-limit throttling

# Send initial messages on startup
send_to_channels(message1, msg1_targets)
time.sleep(2)
send_to_channels(message2, msg2_targets)

# Track last sent timestamps
last_sent_1 = time.time()
last_sent_2 = time.time()

# Main loop checking timers every second
while True:
    now = time.time()

    # Check timer for Message 1 ($rpg boss event)
    if now - last_sent_1 >= interval1:
        send_to_channels(message1, msg1_targets)
        last_sent_1 = now

    # Check timer for Message 2 ($rpg boss battle)
    if now - last_sent_2 >= interval2:
        send_to_channels(message2, msg2_targets)
        last_sent_2 = now

    time.sleep(1)
