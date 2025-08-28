import argparse
import os
import shutil

from bot.logger import logger

def clean(paths: list[str]) -> None:
  for path in paths:
    logger.info(f'Cleaning up {path}')
    for f in os.listdir(path):
      file_path = os.path.join(path, f)
      try:
        if os.path.isfile(file_path):
          logger.debug(f'Removing file {file_path}')
          os.remove(file_path)
        elif os.path.isdir(file_path):
          logger.debug(f'Removing directory {file_path} with all its contents')
          shutil.rmtree(file_path)
      except Exception as e:
        logger.error(f'Error cleaning up {file_path}: {e}')
    logger.info(f'Cleaned up {path}')

def main():
  parser = argparse.ArgumentParser(
    'cleanup',
    description='Cleans up audio and metadata files.  \
    By default cleans only ./downloads/audio/ and ./downloads/metadata/ directories'
  )
  
  parser.add_argument(
    '-p',
    '--path',
    nargs='+',
    type=str,
    required=False,
    help="Additional paths to clean up in format like ./downloads/audio/. \
    Don't clean the directory itself"
  )
  
  args = parser.parse_args()
  
  paths = [
    './downloads/audio',
    './downloads/metadata'
  ]
  
  if args.path:
    paths.extend(args.path)
    
  clean(paths)
  
if __name__ == '__main__':
  main()