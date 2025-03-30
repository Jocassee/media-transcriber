def get_video_urls(file_path="urls.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            urls = [url.strip() for url in content.split(",") if url.strip()]
            return urls
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
