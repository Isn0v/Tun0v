import asyncio
import sys

from bot.logger import logger

STDOUT_REDIRECT = sys.stdout
STDERR_REDIRECT = sys.stderr

# TODO: limit the number of subprocesses if needed
  
async def invoke_async_subprocess(command: str, args: str) -> None:
  logger.info(f'Running async command: {command}')
  process = await asyncio.create_subprocess_exec(
    command,
    *args.split(),
    stdout=STDOUT_REDIRECT,
    stderr=STDERR_REDIRECT
  )
  
  await process.communicate()
  
  if process.returncode != 0:
    logger.error(f'Command {command} failed')
    raise Exception(f'Command {command} failed')