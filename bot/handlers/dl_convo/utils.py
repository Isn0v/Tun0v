from bot.handlers.dl_convo.constants import START_DOWNLOAD_COMMAND


from telegram import ReplyKeyboardMarkup


def get_starter_markup_reply() -> ReplyKeyboardMarkup:
  keyboard = [
    [f'/{START_DOWNLOAD_COMMAND}']
  ]
  return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)