import os
import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

YT_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
FB_REGEX = r"(https?://)?(www\.)?facebook\.com/.+"
IG_REGEX = r"(https?://)?(www\.)?instagram\.com/.+"

@Client.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def link_handler(client: Client, message: Message):
    url = message.text.strip()

    if re.match(YT_REGEX, url):
        platform = "YouTube"
    elif re.match(FB_REGEX, url):
        platform = "Facebook"
    elif re.match(IG_REGEX, url):
        platform = "Instagram"
    else:
        await message.reply_text("❌ দুঃখিত, এই লিংকটি আমি সাপোর্ট করি না।")
        return

    buttons = [
        [
            InlineKeyboardButton("ভিডিও ডাউনলোড", callback_data=f"video|{url}"),
            InlineKeyboardButton("অডিও ডাউনলোড", callback_data=f"audio|{url}"),
        ]
    ]

    await message.reply_text(
        f"✅ শনাক্ত করা হয়েছে: {platform} লিংক।

তুমি কী ডাউনলোড করতে চাও?",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

from pyrogram.types import CallbackQuery
import subprocess
import uuid

@Client.on_callback_query(filters.regex("^(video|audio)\|"))
async def download_handler(client: Client, callback_query: CallbackQuery):
    choice, url = callback_query.data.split("|", 1)
    await callback_query.answer()
    await callback_query.message.edit_text("⬇️ ডাউনলোড শুরু হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")

    download_id = str(uuid.uuid4())[:8]
    filename = f"{download_id}.%(ext)s"
    out_path = f"downloads/{download_id}"
    os.makedirs(out_path, exist_ok=True)

    ytdlp_cmd = [
        "yt-dlp",
        "-o", f"{out_path}/{filename}",
        url
    ]

    if choice == "audio":
        ytdlp_cmd += ["-x", "--audio-format", "mp3"]

    process = await asyncio.create_subprocess_exec(
        *ytdlp_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    files = os.listdir(out_path)
    if not files:
        await callback_query.message.edit_text("❌ ডাউনলোড ব্যর্থ হয়েছে!")
        return

    file_path = os.path.join(out_path, files[0])
    try:
        await callback_query.message.reply_document(
            document=file_path,
            caption=f"✅ সফলভাবে ডাউনলোড হয়েছে!",
        )
        await callback_query.message.delete()
    except Exception as e:
        await callback_query.message.edit_text(f"❌ ফাইল পাঠাতে সমস্যা হয়েছে:
{e}")
    finally:
        try:
            os.remove(file_path)
            os.rmdir(out_path)
        except:
            pass
