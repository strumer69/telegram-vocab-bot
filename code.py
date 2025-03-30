from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import json
import os
import random

# Database (JSON for simplicity)
DB_FILE = "vocabulary_db.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Start Command with Buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Add New", callback_data='add_new')],
        [InlineKeyboardButton("Total Words", callback_data='total_words')],
        [InlineKeyboardButton("Random Ask", callback_data='random_ask')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# Callback for Buttons
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    db = load_db()
    user_id = str(query.from_user.id)
    if user_id not in db:
        db[user_id] = {}
        save_db(db)

    if query.data == 'add_new':
        await query.message.reply_text("Send the word in this format please: `german_word - english_translation`", parse_mode='Markdown')

    elif query.data == 'total_words':
        total_words = len(db[user_id])
        await query.message.reply_text(f"You have {total_words} words in your vocabulary Data Base.")

    elif query.data == 'random_ask':
        if db[user_id]:
            word = random.choice(list(db[user_id].keys()))
            context.user_data['current_word'] = word
            await query.message.reply_text(f"What's the meaning of '{word}'?")
        else:
            await query.message.reply_text("Your vocabulary list is empty.")

# Handle Word Entries
async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    db = load_db()

    if user_id not in db:
        db[user_id] = {}

    if len(context.args) < 3:
        await update.message.reply_text("Usage: /add german_word - english_translation")
        return

    german_word, english_translation = " ".join(context.args).split(' - ')
    db[user_id][german_word.strip()] = english_translation.strip()

    save_db(db)
    await update.message.reply_text(f"Word '{german_word}' added with translation '{english_translation}'!")

# Handle Random Ask Responses
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    db = load_db()

    answer = update.message.text.strip()
    current_word = context.user_data.get('current_word')

    if current_word and db[user_id].get(current_word) == answer:
        await update.message.reply_text("Super! ✅")
    else:
        await update.message.reply_text("😅 Try again!")

    context.user_data.pop('current_word', None)

# Main Application Setup
# app = ApplicationBuilder().token("---").build()
#***********************
import os
from telegram.ext import ApplicationBuilder

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Load from environment

if not TOKEN:
    raise ValueError("Error: TELEGRAM_BOT_TOKEN is not set!")

app = ApplicationBuilder().token(TOKEN).build()

#***********************



app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_word))
app.add_handler(CallbackQueryHandler(button_callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

print("Bot is running...")
app.run_polling()
