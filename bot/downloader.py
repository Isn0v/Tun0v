import yt_dlp


ydl_opts_audio = {
  "outtmpl": "downloads/%(title)s.%(ext)s",
  'format': 'm4a/bestaudio/best',
  'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'm4a'
  }],
}

ydl = yt_dlp.YoutubeDL(ydl_opts_audio)