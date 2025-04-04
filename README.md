
# **📖 Telegram Vocabulary Bot**  

## 📌 Overview  
This is a simple **Telegram bot** designed to help users save and review **German vocabulary with English translations**. The bot stores words in a database and provides interactive features for vocabulary learning.  

## ⚙️ Features  
- **Add new words** (German & English translation) to a database.  
- **Retrieve saved vocabulary** for review.  
- **Interactive quiz mode** (planned feature).  
- **Simple command-based interaction** with Telegram.  

## 🛠 Requirements  
To run this bot, ensure you have the following installed:  

```bash
pip install python-telegram-bot sqlite3
```

## ▶️ Usage  
1. **Clone the repository:**  
   ```bash
   git clone https://github.com/strumer69/telegram-vocab-bot.git
   cd telegram-vocab-bot
   ```
2. **Set up a Telegram Bot Token:**  
   - Create a bot via [BotFather](https://t.me/BotFather).  
   - Get your **API token** and update `code.py` accordingly.  

3. **Run the bot:**  
   ```bash
   python code.py
   ```

4. **Interact with the bot on Telegram** using commands like:  
   - `/add word translation` – Save a new word.  
   - `/list` – View saved words.  

## 🔧 Future Enhancements  
- **GUI buttons** for easier interaction.  
- **Random quiz feature** to test vocabulary.  
- **Deployment on a cloud platform** like PythonAnywhere or Railway.app.  
