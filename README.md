# Satark

Telegram bot that checks suspicious messages, screenshots, voice notes and UPI IDs
for scam red flags and tells you if they were reported before. Built for Hackdays 2.0.

## Live Demo
t.me/Satarkk_bot


## Run it
1. pip install -r requirements.txt
2. Copy .env.example to .env and add your TELEGRAM_BOT_TOKEN
3. python bot.py

## Who owns what
- bot.py, messages.py: Telegram bot and fixed text
- gemini_analysis.py: Gemini analysis (Member 2)
- database.py: SQLite database and verdict logic (Member 3)
- stubs.py: fake versions of the above, for testing


