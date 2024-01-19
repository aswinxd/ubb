# ubmedia.py
from pyrogram import Client
from pyrogram import filters
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config  # Import the Config class from config.py
import os

idss = []

# Specify a shorter session_name
ub = Client(Config.SESSION_STRING, api_id=Config.API_ID, api_hash=Config.API_HASH, sleep_threshold=60, session_name='ub_session')

def clean_data():
    print("checking media")
    for ids in ub.search_messages(chat_id=Config.GROUP_ID, filter="photo_video", limit=20):
        msg_id = ids.message.id
        idss.append(msg_id)
        ub.copy_message(chat_id=Config.CHANNEL_ID, from_chat_id=Config.GROUP_ID, message_id=msg_id)
        ub.delete_messages(chat_id=Config.GROUP_ID, message_ids=[msg_id])

    if len(idss) == 0:
        print("no photos to delete")
    else:
        c = len(idss)
        print(f"cleared almost {c} messages")
        idss.clear()

    for ids in ub.search_messages(chat_id=Config.GROUP_ID, filter="document", limit=5):
        msg_id = ids.message.id
        idss.append(msg_id)
        ub.copy_message(chat_id=Config.CHANNEL_ID, from_chat_id=Config.GROUP_ID, message_id=msg_id)
        ub.delete_messages(chat_id=Config.GROUP_ID, message_ids=[msg_id])

    if len(idss) == 0:
        print("no files to delete")
    else:
        c = len(idss)
        print(f"almost {c} files deleted")
        idss.clear()

def channel_delete():
    print("trying to delete channel messages")
    for ids in ub.search_messages(chat_id=Config.CHANNEL_ID, filter="photo_video"):
        msg_id = ids.message.id
        idss.append(msg_id)
        ub.delete_messages(chat_id=Config.CHANNEL_ID, message_ids=[msg_id])

    if len(idss) == 0:
        print("no photos to delete")
    else:
        c = len(idss)
        print(f"almost {c} files deleted")
        idss.clear()

    for ids in ub.search_messages(chat_id=Config.CHANNEL_ID, filter="document", limit=5):
        msg_id = ids.message.id
        idss.append(msg_id)
        ub.delete_messages(chat_id=Config.CHANNEL_ID, message_ids=[msg_id])

    if len(idss) == 0:
        print("no files to delete")
    else:
        c = len(idss)
        print(f"almost {c} files deleted")
        idss.clear()

scheduler_group = BackgroundScheduler()
scheduler_group.add_job(clean_data, 'interval', seconds=Config.GROUP_DELETE_TIME)
scheduler_group.start()

scheduler_channel = BackgroundScheduler()
scheduler_channel.add_job(channel_delete, 'interval', minutes=Config.CHANNEL_DELETE_TIME)
scheduler_channel.start()

ub.run()
