import requests
import os
import yt_dlp
from pprint import pprint
from get_video_urls import get_video_urls
from download_audio import download_audio
from transcribe_audio import transcribe_audio

#print("Attempting to retrieve urls")
#urls = get_video_urls(file_path="urls.txt")
#print("urls below")
#print(urls)

print("Attempting audio download")
download_audio('https://www.youtube.com/watch?v=qQk94CjRvIs', output_dir="audio")
