import asyncio
import os
import sys

from bot.logger import logger, LOG_PATH

STDOUT_REDIRECT = asyncio.subprocess.PIPE
STDERR_REDIRECT = asyncio.subprocess.PIPE

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
  
  stdout, stderr = await process.communicate()
  
  logger.debug(f'Command {command} {args} exited with code {process.returncode}')
  if os.environ.get('LOG_SUBPROCESSES', 'false') == 'true':
    with open(f'{LOG_PATH}/{args_array[0]}.log', 'a') as f:
      logger.debug(f'Dumping subprocess stdout to {f.name}')
      f.write(stdout.decode('utf-8'))
  
  if process.returncode != 0:
    logger.error(f'Command {command} {args} failed')
    if os.environ.get('LOG_SUBPROCESSES', 'false') == 'true':
      with open(f'{LOG_PATH}/{args_array[0]}.log', 'a') as f:
        logger.debug(f'Dumping subprocess stderr to {f.name}')
        f.write(stderr.decode('utf-8'))
    raise RuntimeError(f'Command {command} {args} failed')