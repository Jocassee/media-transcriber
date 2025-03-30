import os
import yt_dlp

def download_audio(url, output_dir="audio"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{output_dir}/%(id)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "64"
            }],
            "quiet": True,
            "noprogress": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return os.path.join(output_dir, f"{info['id']}.mp3") if info else None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

