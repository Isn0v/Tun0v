import bot.handlers as handlers

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.config import telegram_bot_token


def main():
  application = Application.builder().token(telegram_bot_token).build()
  
  application.add_handler(CommandHandler('start', handlers.start))
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.download_audio))
  
  application.run_polling()

if __name__ == '__main__':
  main()