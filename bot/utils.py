import bot.config as config
from bot.logger import logger


import json
import os


def dump_metadata(filename: str, metadata: dict) -> None:
  metadata_path = f'{config.METADATA_PATH}/{filename}.{config.METADATA_EXT}'
  logger.info(f'Dumping metadata into {os.path.abspath(metadata_path)}')
  with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)

  logger.info('Metadata dumped')


def load_audio(filename: str) -> bytes:
  (audio_path) = f'{config.AUDIO_PATH}/{filename}.{config.AUDIO_EXT}'
  logger.info(f'Loading audio from {os.path.abspath((audio_path))}')
  with open((audio_path), 'rb') as f:
    return f.read()

  logger.info('Audio loaded')