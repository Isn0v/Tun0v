import asyncio
import os
import sys
import config
import json

from logger import logger

#TODO: limit count of async downloads

STDOUT_REDIRECT = sys.stdout
STDERR_REDIRECT = sys.stderr

async def cleanup() -> None:
  logger.info('Cleaning up')
  process = await asyncio.create_subprocess_exec(
    'scripts/cleanup.sh',
    stdout=STDOUT_REDIRECT,
    stderr=STDERR_REDIRECT
  )
  
  await process.communicate()
  
  if process.returncode != 0:
    logger.error('Cleanup failed')
    raise Exception('Cleanup failed')
  
  logger.info('Cleanup finished')

async def download_audio(url: str) -> None:
  logger.info(f'Downloading audio from {url}')
  process = await asyncio.create_subprocess_exec(
    'scripts/download-audio.sh',
    url,
    stdout=STDOUT_REDIRECT,
    stderr=STDERR_REDIRECT
  )
  
  await process.communicate()
  
  if process.returncode != 0:
    logger.error(f'Audio download from {url} failed')
    raise Exception(f'Audio download from {url} failed')
  
  logger.info(f'Audio from {url} downloaded')
  
  
def load_audio(filename: str) -> bytes:
  (audio_path) = f'{config.AUDIO_PATH}/{filename}.{config.AUDIO_EXT}'
  logger.info(f'Loading audio from {os.path.abspath((audio_path))}')
  with open((audio_path), 'rb') as f:
    return f.read()
  
  logger.info('Audio loaded')
  
def dump_metadata(filename: str, metadata: dict) -> None:
  metadata_path = f'{config.METADATA_PATH}/{filename}.{config.METADATA_EXT}'
  logger.info(f'Dumping metadata into {os.path.abspath(metadata_path)}')
  with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
  
  logger.info('Metadata dumped')
