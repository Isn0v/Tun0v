STATES_NUMBER = 10

PLAYLIST_LIMIT = 10

STATES = [i for i in range(STATES_NUMBER)]

DOWNLOAD_OPTIONS = ['Песня', 'Плейлист']

assert len(DOWNLOAD_OPTIONS) <= len(STATES) + 2, "Too many download options for initialization"
