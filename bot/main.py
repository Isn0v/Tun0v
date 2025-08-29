from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot import handlers

import bot.config as config


def main():
  application = Application.builder().token(config.telegram_bot_token).read_timeout(config.BOT_REQUEST_READ_TIMEOUT).build()
  
  conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', handlers.download_start_state_handler)],
    states={
      handlers.STATES[0]: [MessageHandler(filters.TEXT, handlers.download_start_state_handler)],
      handlers.STATES[1]: [MessageHandler(filters.TEXT, handlers.download_option_state_handler)],
      handlers.STATES[2]: [MessageHandler(filters.TEXT, handlers.download_song_state_handler)],
      handlers.STATES[3]: [MessageHandler(filters.TEXT, handlers.download_playlist_state_handler)],
    },
    fallbacks=[CommandHandler('cancel', handlers.cancel_handler)],
  )
  
  application.add_handler(conv_handler)
  application.add_handler(CommandHandler('test', handlers.test_handler))
  
  application.run_polling()

if __name__ == '__main__':
  main()