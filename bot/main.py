from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.handlers import start

import bot.config as config
import bot.handlers.dl_convo.controller


def main():
  assert config.telegram_bot_token is not None, "TELEGRAM_BOT_TOKEN is not set"
  application = Application.builder().token(config.telegram_bot_token).read_timeout(config.BOT_REQUEST_READ_TIMEOUT).build()
  
  conv_handler = bot.handlers.dl_convo.controller.prepare_conversation_handler()
  
  application.add_handler(conv_handler)
  application.add_handler(CommandHandler('test', start.test_handler))
  
  application.run_polling()

if __name__ == '__main__':
  main()