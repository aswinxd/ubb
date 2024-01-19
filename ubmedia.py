# ubmedia.py
from pyrogram import Client
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

idss = []

# Set a custom session storage path
session_path = os.path.join(os.getcwd(), "ub_session")

# Ensure the session_path directory exists
os.makedirs(session_path, exist_ok=True)

# Initialize Pyrogram client with a different approach
ub = Client(
    Config.SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=60,
    app_version="1.0.0",  # Specify your app version
    workdir=session_path
)

def clean_data():
    try:
        logger.info("Checking media")
        
        for ids in ub.search_messages(chat_id=Config.GROUP_ID, filter="photo_video", limit=20):
            msg_id = ids.message.id
            idss.append(msg_id)
            ub.copy_message(chat_id=Config.CHANNEL_ID, from_chat_id=Config.GROUP_ID, message_id=msg_id)
            ub.delete_messages(chat_id=Config.GROUP_ID, message_ids=[msg_id])

        if len(idss) == 0:
            logger.info("No photos to delete")
        else:
            c = len(idss)
            logger.info(f"Cleared almost {c} messages")
            idss.clear()

        for ids in ub.search_messages(chat_id=Config.GROUP_ID, filter="document", limit=5):
            msg_id = ids.message.id
            idss.append(msg_id)
            ub.copy_message(chat_id=Config.CHANNEL_ID, from_chat_id=Config.GROUP_ID, message_id=msg_id)
            ub.delete_messages(chat_id=Config.GROUP_ID, message_ids=[msg_id])

        if len(idss) == 0:
            logger.info("No files to delete")
        else:
            c = len(idss)
            logger.info(f"Almost {c} files deleted")
            idss.clear()

    except Exception as e:
        logger.error(f"An error occurred in clean_data: {e}")

def channel_delete():
    try:
        logger.info("Trying to delete channel messages")

        for ids in ub.search_messages(chat_id=Config.CHANNEL_ID, filter="photo_video"):
            msg_id = ids.message.id
            idss.append(msg_id)
            ub.delete_messages(chat_id=Config.CHANNEL_ID, message_ids=[msg_id])

        if len(idss) == 0:
            logger.info("No photos to delete")
        else:
            c = len(idss)
            logger.info(f"Almost {c} files deleted")
            idss.clear()

        for ids in ub.search_messages(chat_id=Config.CHANNEL_ID, filter="document", limit=5):
            msg_id = ids.message.id
            idss.append(msg_id)
            ub.delete_messages(chat_id=Config.CHANNEL_ID, message_ids=[msg_id])

        if len(idss) == 0:
            logger.info("No files to delete")
        else:
            c = len(idss)
            logger.info(f"Almost {c} files deleted")
            idss.clear()

    except Exception as e:
        logger.error(f"An error occurred in channel_delete: {e}")

scheduler_group = BackgroundScheduler()
scheduler_group.add_job(clean_data, 'interval', seconds=Config.GROUP_DELETE_TIME)
scheduler_group.start()

scheduler_channel = BackgroundScheduler()
scheduler_channel.add_job(channel_delete, 'interval', minutes=Config.CHANNEL_DELETE_TIME)
scheduler_channel.start()

try:
    ub.run()
except Exception as e:
    logger.error(f"An error occurred in ub.run(): {e}")
