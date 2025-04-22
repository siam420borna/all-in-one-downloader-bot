from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    await message.reply_text(
        text="👋 হ্যালো! আমি All In One Downloader Bot।

যেকোনো YouTube, Facebook, Instagram লিংক সেন্ড করো—আমি ডাউনলোড লিংক/ফাইল দিয়ে দিবো!",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ডেভেলপার", url="https://t.me/YourUsername")],
                [InlineKeyboardButton("চ্যানেল", url="https://t.me/YourChannel")],
            ]
        )
    )
