from pyrogram import Client
from pyrogram import filters
from apscheduler.schedulers.background import BackgroundScheduler
import os
from os import getenv

# Heroku Config Variables
api_id_heroku = int(getenv("API_ID"))
api_hash_heroku = getenv("API_HASH")
string_heroku = getenv("SESSION_STRING")
g_time = int(getenv("GROUP_DELETE_TIME"))
c_time = int(getenv("CHANNEL_DELETE_TIME"))
group = int(getenv("GROUP_ID"))
channel = int(getenv("CHANNEL_ID"))

# Pyrogram Config Variables
api_id_pyrogram = api_id_heroku
api_hash_pyrogram = api_hash_heroku
string_pyrogram = string_heroku

idss = []

ub = Client(string_pyrogram, api_id=api_id_pyrogram, api_hash=api_hash_pyrogram, sleep_threshold=60)

def clean_data():
    print("checking media")
    for ids in ub.search_messages(chat_id=group, filter="photo_video", limit=20):
        msg_id = ids.message.id  # consistent naming
        idss.append(msg_id)
        ub.copy_message(chat_id=channel, from_chat_id=group, message_id=msg_id)
        ub.delete_messages(chat_id=group, message_ids=[msg_id])  # Corrected typo here
    
    if len(idss) == 0:
        print("no photos to delete")
    else:
        c = len(idss)
        print(f"cleared almost {c} messages")
        idss.clear()

    for ids in ub.search_messages(chat_id=group, filter="document", limit=5):
        msg_id = ids.message.id  # consistent naming
        idss.append(msg_id)
        ub.copy_message(chat_id=channel, from_chat_id=group, message_id=msg_id)
        ub.delete_messages(chat_id=group, message_ids=[msg_id])  # Corrected typo here
    
    if len(idss) == 0:
        print("no files to delete")
    else:
        c = len(idss)
        print(f"almost {c} files deleted")
        idss.clear()

def channel_delete():
    print("trying to delete channel messages")
    for ids in ub.search_messages(chat_id=channel, filter="photo_video"):
        msg_id = ids.message.id  # consistent naming
        idss.append(msg_id)
        ub.delete_messages(chat_id=channel, message_ids=[msg_id])  # Corrected typo here

    if len(idss) == 0:
        print("no photos to delete")
    else:
        c = len(idss)
        print(f"almost {c} files deleted")
        idss.clear()

    for ids in ub.search_messages(chat_id=channel, filter="document", limit=5):
        msg_id = ids.message.id  # consistent naming
        idss.append(msg_id)
        ub.delete_messages(chat_id=channel, message_ids=[msg_id])  # Corrected typo here
    
    if len(idss) == 0:
        print("no files to delete")
    else:
        c = len(idss)
        print(f"almost {c} files deleted")
        idss.clear()

# Use different variable names for the two schedulers
scheduler_group = BackgroundScheduler()
scheduler_group.add_job(clean_data, 'interval', seconds=g_time)
scheduler_group.start()

scheduler_channel = BackgroundScheduler()
scheduler_channel.add_job(channel_delete, 'interval', minutes=c_time)
scheduler_channel.start()

ub.run()
