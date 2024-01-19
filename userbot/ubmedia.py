# ubmedia.py
from pyrogram import Client
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config

class MediaBot(Client):
    def __init__(self, name, config):
        super().__init__(
            config.SESSION_STRING,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            sleep_threshold=60,
            parse_mode="markdown",
        )
        self.name = name
        self.config = config
        self.scheduler = BackgroundScheduler()

        # Add jobs to the scheduler
        self.scheduler.add_job(self.clean_data, 'interval', seconds=config.GROUP_DELETE_TIME)
        self.scheduler.add_job(self.channel_delete, 'interval', minutes=config.CHANNEL_DELETE_TIME)

        # Start the scheduler
        self.scheduler.start()

    def clean_data(self):
        print(f"[{self.name}] Checking media")
        idss = []

        for ids in self.search_messages(chat_id=self.config.GROUP_ID, filter="photo_video", limit=20):
            msg_id = ids.message_id
            idss.append(msg_id)
            self.copy_message(chat_id=self.config.CHANNEL_ID, from_chat_id=self.config.GROUP_ID, message_id=msg_id)
            self.delete_messages(chat_id=self.config.GROUP_ID, message_ids=msg_id)
        else:
            if not idss:
                print("No photos to delete")
            else:
                c = len(idss)
                print(f"Cleared almost {c} messages")
                idss.clear()

        for ids in self.search_messages(chat_id=self.config.GROUP_ID, filter="document", limit=5):
            msg_id = ids.message_id
            idss.append(msg_id)
            self.copy_message(chat_id=self.config.CHANNEL_ID, from_chat_id=self.config.GROUP_ID, message_id=msg_id)
            self.delete_messages(chat_id=self.config.GROUP_ID, message_ids=msg_id)
        else:
            if not idss:
                print("No files to delete")
            else:
                c = len(idss)
                print(f"Almost {c} files deleted")
                idss.clear()

    def channel_delete(self):
        print(f"[{self.name}] Trying to delete channel messages")
        idss = []

        for ids in self.search_messages(chat_id=self.config.CHANNEL_ID, filter="photo_video"):
            msg_id = ids.message_id
            idss.append(msg_id)
            self.delete_messages(chat_id=self.config.CHANNEL_ID, message_ids=msg_id)
        else:
            if not idss:
                print("No photos to delete")
            else:
                c = len(idss)
                print(f"Almost {c} files deleted")
                idss.clear()

        for ids in self.search_messages(chat_id=self.config.CHANNEL_ID, filter="document", limit=5):
            msg_id = ids.message_id
            idss.append(msg_id)
            self.delete_messages(chat_id=self.config.CHANNEL_ID, message_ids=msg_id)
        else:
            if not idss:
                print("No files to delete")
            else:
                c = len(idss)
                print(f"Almost {c} files deleted")
                idss.clear()

    def run(self):
        try:
            print(f"[{self.name}] Starting...")
            super().run()
        finally:
            print(f"[{self.name}] Stopping...")
            self.scheduler.shutdown()

# Initialize and run the bot
ub = MediaBot("ub", Config)
ub.run()
