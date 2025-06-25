# bot.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, Application

# Telegram Bot Token
TOKEN = "7429762049:AAEq4iAITSkIFlohNRu0le4Vtt0U2xILUiw"

# Button layouts
agree_menu = ReplyKeyboardMarkup([[KeyboardButton("✅ Agree 💯")]], resize_keyboard=True)

main_menu = ReplyKeyboardMarkup([
    ["🕵️ URL Masking (Cloaking)"],
    ["👨‍💻 Developer Info"]
], resize_keyboard=True)

# Track user state (reset on restart)
user_state = {}

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_state[user_id] = "AGREE"
    await update.message.reply_text(
        "📢 Assalamualaikum.\n"
        "Welcome to Link Masking (Beta).\n"
        "With this bot you can mask/ cloak any URL.\n\n"
        "Dear Nayeem Hussain,\n"
        "If you want to use this bot, you must follow the following rules:\n\n"
        "⚠️ Do not harm anyone by using this bot.\n"
        "If you have harmed someone, then the responsibility is entirely yours.\n\n"
        "🤖 Bot Developer: Nayeem Hussain\n"
        "📢 Channel: https://t.me/VoiceOfDhakaVideoEditingCourse\n\n"
        "Do you accept these policies?\n"
        "Then please click the button below 👇",
        reply_markup=agree_menu
    )

# Handle all user replies
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_state:
        await start(update, context)
        return

    state = user_state.get(user_id)

    if state == "AGREE":
        if text == "✅ Agree 💯":
            user_state[user_id] = "MENU"
            await update.message.reply_text("✅ আপনি শর্ত মেনে নিয়েছেন। নিচে থেকে একটি অপশন বেছে নিন 👇", reply_markup=main_menu)
        else:
            await update.message.reply_text("❌ দয়া করে '✅ Agree 💯' বাটনে ক্লিক করুন!")
        return

    if state == "MENU":
        if text == "🕵️ URL Masking (Cloaking)":
            user_state[user_id] = "MASK_INPUT"
            await update.message.reply_text("🕵️ Send your URL without https:// or http:// :")
        elif text == "👨‍💻 Developer Info":
            await update.message.reply_text("👨‍💻 Developer: Nayeem Hussain\n📢 Channel: https://t.me/VoiceOfDhakaVideoEditingCourse")
        else:
            await update.message.reply_text("❓ অপশন বুঝিনি। দয়া করে নিচের বোতামগুলো ব্যবহার করুন।")
        return

    if state == "MASK_INPUT":
        raw = text.strip().replace("https://", "").replace("http://", "")
        if not raw:
            await update.message.reply_text("❌ কোনো লিংক পাওয়া যায়নি। আবার চেষ্টা করুন।")
            return

        platforms = {
            "🔴 YouTube": "https://youtube.com@",
            "🟢 Google": "https://google.com@",
            "🟡 Play Store": "https://play.google.com@",
            "🔵 Facebook": "https://facebook.com@",
            "💬 Telegram": "https://t.me@",
            "📱 WhatsApp": "https://wa.me@",
            "📂 Google Drive": "https://drive.google.com@",
            "📦 Terabox App": "https://teraboxapp.com@",
            "🗃️ Terabox": "https://terabox.com@"
        }

        response = "🔗 Your Masked URLs:\n\n"
        for name, base in platforms.items():
            response += f"{name} = {base}{raw}\n"

        response += "\n🤖 Bot by: Nayeem Hussain"
        await update.message.reply_text(response, reply_markup=main_menu)
        user_state[user_id] = "MENU"
        return
