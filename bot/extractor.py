import config
import json
from typing import Callable

def extract_song(metadata: dict) -> str:
  name = f'{metadata["artist"]} - {metadata["title"]} [{metadata["album"]["name"]}]'
  link = f'{config.SONG_URL_TEMPLATE.format(metadata["videoId"])}'
  return f'[{name}]({link})'


def extract_playlist(metadata: dict) -> str:
  # TODO
  raise NotImplementedError


filter_to_extractor : dict[str, Callable[[dict], str]] = {
  'songs': extract_song,
  'playlists': extract_playlist
}

def search_then_dump(query: str, filter: str) -> None:
  songs = config.ytmusic.search(query, filter=filter, limit=1)

  with open(f']{config.METADATA_PATH}/{config.METADATA_NAME}.{config.METADATA_EXT}', 'w') as f:
    json.dump(songs, f, indent=2)
    
    
def extract_after_dump(filter: str) -> str:
  '''
  Extracts information about songs which were prevously searched by search_then_dump method 
  and returns list of hyperlinks in markdown format
  '''
  
  extractor = filter_to_extractor[filter]
  metadata = {}
  
  with open(f'{config.METADATA_PATH}/{config.METADATA_NAME}.{config.METADATA_EXT}', 'r') as f:
    metadata = json.load(f)
  
  return extractor(metadata)
  
def extract_info(query: str, filter: str) -> str:
  search_then_dump(query, filter)
  return extract_after_dump(filter)
