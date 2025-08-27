import asyncio
import sys

#TODO: limit count of async downloads

STDOUT_REDIRECT = sys.stdout
STDERR_REDIRECT = sys.stderr

async def cleanup() -> None:
  process = await asyncio.create_subprocess_exec(
    'scripts/cleanup.sh',
    stdout=STDOUT_REDIRECT,
    stderr=STDERR_REDIRECT
  )
  
  await process.communicate()
  
  if process.returncode != 0:
    raise Exception('Cleanup failed')

async def download_audio(url: str) -> None:
  process = await asyncio.create_subprocess_exec(
    'scripts/download-audio.sh',
    url,
    stdout=STDOUT_REDIRECT,
    stderr=STDERR_REDIRECT
  )
  
  await process.communicate()
  
  if process.returncode != 0:
    raise Exception('Audio download failed')
  