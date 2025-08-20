import asyncio
import json
import os
import config

async def cleanup() -> None:
  process = await asyncio.create_subprocess_exec(
    'scripts/cleanup.sh',
    cwd=os.getcwd(),
    stdout=asyncio.subprocess.PIPE
  )
  
  await process.communicate()
  
  if process.returncode != 0:
    raise Exception('Cleanup failed')

async def download_audio(url: str) -> None:
  process = await asyncio.create_subprocess_exec(
    'scripts/download-audio.sh',
    url,
    cwd=os.getcwd(),
    stdout=asyncio.subprocess.PIPE
  )
  
  await process.communicate()
  
  if process.returncode != 0:
    raise Exception('Audio download failed')
  
async def download_audio_info(url: str) -> None:
  process = await asyncio.create_subprocess_exec(
    'scripts/get-audio-info.sh',
    url,
    cwd=os.getcwd(),
    stdout=asyncio.subprocess.PIPE
  )
  
  await process.communicate()
  
  if process.returncode != 0:
    raise Exception('Audio info download failed')
  
  
def load_metadata() -> dict:
  with open(f'{config.METADATA_PATH}/{config.METADATA_NAME}.{config.METADATA_JSON_EXT}', 'r') as f:
    return json.load(f)