from bot.handlers.dl_convo.utils import get_starter_markup_reply
from bot.logger import logger


from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def cancel_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Leaving the conversation')

  if not update.message or not update.effective_user:
    logger.error('Incorrect state of user or message for download start handler. Quitting the conversation...')
    return ConversationHandler.END

  reply = 'Взвращаюсь в главное меню'
  await update.message.reply_text(reply, reply_markup=get_starter_markup_reply())

  return ConversationHandler.END