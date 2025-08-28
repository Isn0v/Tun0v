import config

from config import ytmusic
from logger import logger

def search_metadata(query: str, filter: str) -> dict:
  logger.debug(f'Searching for {query} with filter {filter}')
  metadata = config.ytmusic.search(query, filter=filter, limit=1)
  if metadata:
    logger.debug(f'Found search result for {query}')
    return metadata[0]
  else:
    logger.debug(f'No search result found for {query}')
    return {}
  
def search_song_metadata(query: str) -> dict:
  logger.debug(f'Searching for song with query {query}')
  return search_metadata(query, 'songs')

def search_playlist_metadata(query: str) -> dict:
  logger.debug(f'Searching for playlist with query {query}')
  search_result = search_metadata(query, 'playlists')
  
  logger.debug(f'Found playlist with query {query}')
  playlist = ytmusic.get_playlist(get_browse_id(search_result))
  
  return playlist

def get_browse_id(metadata: dict) -> str:
  logger.debug(f'Extracting browse id')
  browse_id = metadata['browseId']
  logger.debug(f'Extracted browse id: {browse_id}')
  return browse_id