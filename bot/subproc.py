import asyncio
import os
import sys

from bot.logger import logger, LOG_PATH

STDOUT_REDIRECT = asyncio.subprocess.PIPE
STDERR_REDIRECT = asyncio.subprocess.PIPE

LOG_SUBPROCESSES = os.environ.get('LOG_SUBPROCESSES', 'false')
logger.debug(f"LOG_SUBPROCESSES: {LOG_SUBPROCESSES}")

async def log_subprocess_stream(stream: asyncio.StreamReader, logger_function) -> None:
  while True:
    stdout_line = await stream.readline()
    if stdout_line:
      stdout_line = stdout_line.rstrip(b'\n')
    if not stdout_line:
      break
    logger_function(stdout_line.decode('utf-8'))


# TODO: limit the number of subprocesses if needed
  
async def invoke_async_subprocess(command: str, args: str) -> None:
  logger.info(f'Running async command: {command} {args}')
  args_array = args.split()
  process = await asyncio.create_subprocess_exec(
    command,
    *args_array,
    stdout=STDOUT_REDIRECT,
    stderr=STDERR_REDIRECT,
    env=os.environ.copy()
  )
  
  if process.stdout:
    await log_subprocess_stream(process.stdout, logger.debug)
  if process.stderr:
    await log_subprocess_stream(process.stderr, logger.error)
  
  await process.communicate()
  
  if process.returncode != 0:
    logger.error(f'Command {command} {args} failed')
    raise RuntimeError(f'Command {command} {args} failed')