import logging
from pyrogram import Client
from config import Config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

plugins = dict(root="plugins")

app = Client(
    "AllInOneDownloader",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=plugins
)

if __name__ == "__main__":
    logging.info("Bot Started...")
    app.run()
