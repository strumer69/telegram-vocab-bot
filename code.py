from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import json
import os
import random

# #*************************to connect to postgre_DataBase
# import psycopg2 
# # Load the database URL from Railway environment variables
# DATABASE_URL = os.getenv("DATABASE_URL")
# # Connect to PostgreSQL
# conn = psycopg2.connect(DATABASE_URL)
# cur = conn.cursor()

# # Create a table (run this once)
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS vocabulary (
#         id SERIAL PRIMARY KEY,
#         user_id TEXT,
#         german_word TEXT,
#         english_translation TEXT
#     )
# """)
# conn.commit()

# # Function to add words
# def add_word(user_id, german_word, english_translation):
#     cur.execute("INSERT INTO vocabulary (user_id, german_word, english_translation) VALUES (%s, %s, %s)",
#                 (user_id, german_word, english_translation))
#     conn.commit()

# # Function to get total word count
# def get_word_count(user_id):
#     cur.execute("SELECT COUNT(*) FROM vocabulary WHERE user_id = %s", (user_id,))
#     return cur.fetchone()[0]
#*************************

# ************************** Database (JSON for simplicity) **************************
DB_FILE = "vocabulary_db.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump({}, f)


#*********************** load DB **************************
def load_db():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

#*********************** save DB **************************
def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# *******************************Start Command with Buttons **************************
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Add New", callback_data='add_new')],
        [InlineKeyboardButton("Total Words", callback_data='total_words')],
        [InlineKeyboardButton("Random Ask", callback_data='random_ask')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)


# ***************************Callback for Buttons ******************************
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    db = load_db()
    user_id = str(query.from_user.id)
    if user_id not in db:
        db[user_id] = {}
        save_db(db)

    if query.data == 'add_new':
        await query.message.reply_text("Send the word in this format : `german - english`", parse_mode='Markdown')

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


# ************************** Handle Word Entries **************************
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


# ************************** Handle Random Ask Responses **************************
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    db = load_db()

    answer = update.message.text.strip()
    current_word = context.user_data.get('current_word')

    if current_word and db[user_id].get(current_word) == answer:
        await update.message.reply_text("Super! ✅")
    else:
        await update.message.reply_text(" Try again!")

    context.user_data.pop('current_word', None)

# Main Application Setup

#************************** for local running **************************
# app = ApplicationBuilder().token("---").build()

#*********************** for remote server run **************************
TOKEN = os.getenv("BOT_TOKEN")  # Load from environment

if not TOKEN:
    raise ValueError("Error: BOT_TOKEN is not set!")

app = ApplicationBuilder().token(TOKEN).build()

#***********************



app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_word))
app.add_handler(CallbackQueryHandler(button_callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

print("Bot is running...")
app.run_polling()


    
