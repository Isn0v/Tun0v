from typing import Callable

from telegram.helpers import escape_markdown

from bot.logger import logger
import bot.utils as utils

SONG_URL_TEMPLATE = 'https://music.youtube.com/watch?v={}'
PLAYLIST_URL_TEMPLATE = 'https://music.youtube.com/playlist?list={}'

# TODO: extract method must be async
def extract(metadata: dict, filter: str) -> str:
  logger.debug(f'Extracting metadata with filter {filter}')
  extractor = filter_to_extractor[filter]
  
  return extractor(metadata)

# region Song Metadata Extraction
def extract_song(metadata: dict) -> str:
  logger.debug(f'Extracting song metadata')
  
  album = escape_markdown(get_song_album(metadata), version=2)
  song_title = escape_markdown(get_song_title(metadata), version=2)
  song_performers = escape_markdown(get_song_performers(metadata), version=2)
  
  name = f'{song_title} \\- {song_performers} \\[{album}\\]'
  if album == "":
      name = f'{get_song_title(metadata)} - {get_song_performers(metadata)}'

  link = format_song_url(get_song_video_id(metadata))
  
  extracted = f'[{name}]({link})\n'
  logger.debug(f'Extracted song metadata: {extracted}')
  return extracted

def get_song_duration(metadata: dict) -> int:
  logger.debug(f'Extracting song duration')
  extracted = metadata['duration_seconds']
  logger.debug(f'Extracted song duration: {extracted}')
  return extracted

def get_song_performers(metadata: dict) -> str:
  logger.debug(f'Extracting song performers')
  performers = ''
  for artist in metadata['artists']:
    performers += f'{artist["name"]}, '
  performers = performers[:-2]
  extracted = performers
  logger.debug(f'Extracted song performers: {extracted}')
  return extracted

def get_song_title(metadata: dict) -> str:
  logger.debug(f'Extracting song title')
  extracted = metadata['title']
  logger.debug(f'Extracted song title: {extracted}')
  return extracted

def get_song_thumbnail_url(metadata: dict) -> str:
  logger.debug(f'Extracting song thumbnail')
  extracted = metadata['thumbnails'][0]['url']
  logger.debug(f'Extracted song thumbnail: {extracted}')
  return extracted

def get_song_album(metadata: dict) -> str:
  logger.debug(f'Extracting song album')
  if not metadata['album']:
    logger.debug(f'No song album found')
    return ''
  
  extracted = metadata['album']['name']
  logger.debug(f'Extracted song album: {extracted}')
  return extracted

def get_song_video_id(metadata: dict) -> str:
  logger.debug(f'Extracting song video id')
  extracted = metadata['videoId']
  logger.debug(f'Extracted song video id: {extracted}')
  return extracted

def format_song_url(video_id: str) -> str:
  logger.debug(f'Formatting song url with video id {video_id}')
  song_url = SONG_URL_TEMPLATE.format(video_id)
  extracted = song_url
  logger.debug(f'Formatted song url: {extracted}')
  return extracted
# endregion

# region Playlist Metadata Extraction
def extract_playlist(metadata: dict) -> str:
  logger.debug(f'Extracting playlist metadata')
  name = get_playlist_title(metadata)
  link = format_playlist_url(get_playlist_id(metadata))
  
  tracks = ''
  for i, song in enumerate(metadata['tracks']):
    tracks += f'{i + 1}\\. {extract_song(song)}'
    
  description = get_playlist_description(metadata)
  if description:
    description = 'Описание:\n' + \
        f'{description}\n'
  
  extracted = f'[{name}]({link}):\n' + \
        description + \
        'Треки:\n' + \
        f'{tracks}'
  logger.debug(f'Extracted playlist metadata: {extracted}')
  return extracted

def get_playlist_track_video_ids(metadata: dict) -> list[str]:
  logger.debug(f'Extracting playlist track ids')
  track_ids = []
  for song in metadata['tracks']:
    track_ids.append(get_song_video_id(song))
  logger.debug(f'Extracted playlist track ids: {track_ids}')
  return track_ids

def get_playlist_track_metadata(metadata: dict) -> list[dict]:
  logger.debug(f'Extracting playlist tracks metadata')
  tracks_metadata = metadata['tracks']
  logger.debug(f'Extracted playlist track metadata: {tracks_metadata}')
  return tracks_metadata

def get_playlist_id(metadata: dict) -> str:
  logger.debug(f'Extracting playlist id')
  playlist_id = metadata['id']
  logger.debug(f'Extracted playlist id: {playlist_id}')
  return playlist_id

def get_playlist_title(metadata: dict) -> str:
  logger.debug(f'Extracting playlist title')
  title = metadata['title']
  logger.debug(f'Extracted playlist title: {title}')
  return title

def get_playlist_description(metadata: dict) -> str:
  logger.debug(f'Extracting playlist description')
  description = metadata['description']
  if not description:
    logger.debug(f'No playlist description found')
    description = ''
  logger.debug(f'Extracted playlist description: {description}')
  return description

def get_playlist_duration(metadata: dict) -> str:
  logger.debug(f'Extracting playlist duration')
  duration = metadata['duration']
  logger.debug(f'Extracted playlist duration: {duration}')
  return duration

def format_playlist_url(playlist_id: str) -> str:
  logger.debug(f'Formatting playlist url with playlist id {playlist_id}')
  playlist_url = PLAYLIST_URL_TEMPLATE.format(playlist_id)
  logger.debug(f'Formatted playlist url: {playlist_url}')
  return playlist_url
# endregion


filter_to_extractor : dict[str, Callable[[dict], str]] = {
  'song': extract_song,
  'playlist': extract_playlist
}


def get_browse_id(metadata: dict) -> str:
  logger.debug(f'Extracting browse id')
  browse_id = metadata['browseId']
  logger.debug(f'Extracted browse id: {browse_id}')
  return browse_id
