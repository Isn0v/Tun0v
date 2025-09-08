from bot.handlers.dl_convo.constants import (CANCEL_DOWNLOAD_COMMAND, DOWNLOAD_START_STATE,
                                            DOWNLOAD_OPTION_STATE,
                                            RETRIEVE_METADATA_STATE,
                                            DOWNLOAD_SONG_STATE,
                                            START_DOWNLOAD_COMMAND)

from bot.handlers.dl_convo.download_option_state_handler import download_option_state_handler
from bot.handlers.dl_convo.download_song_state_handler import download_song_state_handler
from bot.handlers.dl_convo.download_start_state_handler import download_start_state_handler
from bot.handlers.dl_convo.retrieve_metadata_song_state_handler import retrieve_metadata_song_state_handler

from bot.logger import logger

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters


def prepare_conversation_handler() -> ConversationHandler:
  """
  Prepares the conversation handler for the download conversation.

  The conversation handler consists of the following states:

  1. DOWNLOAD_START: The entry point of the conversation.
  2. DOWNLOAD_OPTIONS: The state where the user is asked to select
                            what to download (song or playlist).
  3. RETRIEVE_METADATA: The state where the metadata of the
                            selected option is retrieved. 
                            Method is named as retrieve_metadata_<option_name>_state_handler
  4. DOWNLOAD: The state where the selected option is downloaded. 
                            Method is named as download_<option_name>_state_handler
  # TODO: state for choosing between search results
  5. END (reserved number): The state where the conversation ends.

  Returns:
    ConversationHandler: The prepared conversation handler.
  """

  # TODO: playlist option
  return ConversationHandler(
    entry_points=[CommandHandler(START_DOWNLOAD_COMMAND, download_start_state_handler)],
    states={
      DOWNLOAD_START_STATE: [MessageHandler(filters.TEXT, download_start_state_handler)],
      DOWNLOAD_OPTION_STATE: [MessageHandler(filters.TEXT, download_option_state_handler)],
      RETRIEVE_METADATA_STATE: [MessageHandler(filters.TEXT, retrieve_metadata_song_state_handler)],
      DOWNLOAD_SONG_STATE: [MessageHandler(filters.TEXT, download_song_state_handler)],
    },
    fallbacks=[CommandHandler(CANCEL_DOWNLOAD_COMMAND, cancel_handler)],
  )


async def cancel_handler(update: Update, context: CallbackContext) -> int:
  logger.info('Leaving the conversation')
  # TODO setup a reply from with basic markup
  return ConversationHandler.END
