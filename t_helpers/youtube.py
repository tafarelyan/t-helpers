import requests
import youtube_dl
from bs4 import BeautifulSoup


def download_from_youtube(text):
    url = 'https://www.youtube.com'
    r = requests.get('{}/results?search_query={}'.format(url, text))
    soup = BeautifulSoup(r.content, 'html.parser')
    for tag in soup.find_all('a', {'rel': 'spf-prefetch'}):
        title, video_url = tag.text, url + tag['href']
        if 'googleads' not in video_url:
            break

    ydl_opts = {
        'outtmpl': title + '.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
