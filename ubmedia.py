# ubmedia.py
from pyrogram import Client
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
import os

idss = []


# Initialize Pyrogram client
ub = Client(
    Config.SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=60,
    app_version="1.0.0",  # Specify your app version
    workdir=session_path
)

def clean_data():
    print("Checking media")
    for ids in ub.search_messages(chat_id=Config.GROUP_ID, filter="photo_video", limit=20):
        msg_id = ids.message_id
        idss.append(msg_id)
        ub.copy_message(chat_id=Config.CHANNEL_ID, from_chat_id=Config.GROUP_ID, message_id=msg_id)
        ub.delete_messages(chat_id=Config.GROUP_ID, message_ids=msg_id)
    else:
        if not idss:
            print("No photos to delete")
        else:
            c = len(idss)
            print(f"Cleared almost {c} messages")
            idss.clear()

    for ids in ub.search_messages(chat_id=Config.GROUP_ID, filter="document", limit=5):
        msg_id = ids.message_id
        idss.append(msg_id)
        ub.copy_message(chat_id=Config.CHANNEL_ID, from_chat_id=Config.GROUP_ID, message_id=msg_id)
        ub.delete_messages(chat_id=Config.GROUP_ID, message_ids=msg_id)
    else:
        if not idss:
            print("No files to delete")
        else:
            c = len(idss)
            print(f"Almost {c} files deleted")
            idss.clear()

def channel_delete():
    print("Trying to delete channel messages")
    for ids in ub.search_messages(chat_id=Config.CHANNEL_ID, filter="photo_video"):
        msg_id = ids.message_id
        idss.append(msg_id)
        ub.delete_messages(chat_id=Config.CHANNEL_ID, message_ids=msg_id)
    else:
        if not idss:
            print("No photos to delete")
        else:
            c = len(idss)
            print(f"Almost {c} files deleted")
            idss.clear()

    for ids in ub.search_messages(chat_id=Config.CHANNEL_ID, filter="document", limit=5):
        msg_id = ids.message_id
        idss.append(msg_id)
        ub.delete_messages(chat_id=Config.CHANNEL_ID, message_ids=msg_id)
    else:
        if not idss:
            print("No files to delete")
        else:
            c = len(idss)
            print(f"Almost {c} files deleted")
            idss.clear()

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Add jobs to the scheduler
scheduler.add_job(clean_data, 'interval', seconds=Config.GROUP_DELETE_TIME)
scheduler.add_job(channel_delete, 'interval', minutes=Config.CHANNEL_DELETE_TIME)

# Start the scheduler
scheduler.start()

# Run the Pyrogram client
ub.run()
