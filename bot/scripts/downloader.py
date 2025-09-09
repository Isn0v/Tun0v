import yt_dlp
import argparse

from bot.config import AUDIO_EXT, AUDIO_PATH

from bot.logger import logger

default_ydl_opts = {
  'format': f'{AUDIO_EXT}/bestaudio/best',
  'outtmpl': {
    'default': 'TO_BE_OVERRIDEN', 
    'pl_thumbnail': ''
    },
  'postprocessors': [{
                      'add_chapters': True,
                      'add_infojson': 'if_exists',
                      'add_metadata': True,
                      'key': 'FFmpegMetadata'
                    },
                    {
                      'already_have_thumbnail': False, 
                      'key': 'EmbedThumbnail'
                    }],
  'writethumbnail': True
}



def download_songs(songs: list[str]) -> None:
  ydl_song_opts = default_ydl_opts.copy()
  ydl_song_opts['outtmpl']['default'] = f'{AUDIO_PATH}/%(id)s.{AUDIO_EXT}'
  
  ydl = yt_dlp.YoutubeDL(ydl_song_opts)
  ydl.download(songs)
  
def download_playlist(playlist_url: str) -> None:
  ydl_playlist_opts = default_ydl_opts.copy()
  ydl_playlist_opts['outtmpl']['default'] = f'{AUDIO_PATH}/%(playlist_id)s/%(id)s.{AUDIO_EXT}',
  
  ydl = yt_dlp.YoutubeDL(ydl_playlist_opts)
  
  ydl.download([playlist_url])

def main() -> None:
  parser = argparse.ArgumentParser(
    'downloader',
    description='Downloader from YouTube',
  )
  
  parser.add_argument(
    '-s',
    '--song-url',
    nargs='+',
    type=str,
    help='Song URL to download'
  )
  
  parser.add_argument(
    '-p',
    '--playlist-url',
    type=str,
    help='Playlist URL to download'
  )
  
  args = parser.parse_args()
  
  if not (args.song_url or args.playlist_url):
    logger.error('No song or playlist URL provided')
    return
  
  if args.song_url:
    download_songs(args.song_url)
  
  if args.playlist_url:
    download_playlist(args.playlist_url)
    
    
if __name__ == '__main__':
  main()