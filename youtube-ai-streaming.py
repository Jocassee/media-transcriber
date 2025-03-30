import subprocess
import whisper
import numpy as np
import soundfile as sf
import io
import torch

def transcribe_stream(url, model_size="small", chunk_size=1024 * 64):
    try:
        # Load Whisper model in FP16 and move to GPU
        model = whisper.load_model(model_size).to("cuda").half()
        print("Model loaded on:", next(model.parameters()).device)  # Debugging output

        # yt-dlp streams best audio, ffmpeg converts it to WAV
        command = [
            "yt-dlp", "-f", "bestaudio", "-o", "-",
            url, "|", 
            "ffmpeg", "-i", "pipe:0", "-f", "wav", "-ac", "1", "-ar", "16000", "pipe:1"
        ]

        # Open a subprocess with proper piping
        process = subprocess.Popen(
            " ".join(command),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=10**6  # Large buffer for long videos
        )

        audio_data = io.BytesIO()

        # Read audio in chunks to avoid memory overload
        while True:
            chunk = process.stdout.read(chunk_size)
            if not chunk:
                break
            audio_data.write(chunk)

        # Check for errors in stderr (ffmpeg may fail)
        stderr_output = process.stderr.read().decode()
        if stderr_output:
            print("FFmpeg Error Log:", stderr_output)

        if len(audio_data.getvalue()) == 0:
            raise ValueError("Received empty audio stream. yt-dlp or ffmpeg may have failed.")

        # Reset buffer position
        audio_data.seek(0)

        # Convert audio stream to NumPy array (must be FP32 for Whisper)
        try:
            audio_array, sample_rate = sf.read(audio_data, dtype="float32")
        except Exception as sf_error:
            print("SoundFile Error:", sf_error)
            raise ValueError("Audio format issue. Check if ffmpeg is correctly processing the stream.")

        # Convert audio to PyTorch tensor and keep it in FP32
        audio_tensor = torch.tensor(audio_array, dtype=torch.float32).to("cuda")

        # Use automatic mixed precision to avoid FP16 errors
        with torch.autocast("cuda", dtype=torch.float16):
            result = model.transcribe(audio_tensor)

        return result["text"]

    except Exception as e:
        print(f"Error: {e}")
        return None
# Example usage
url = "https://www.youtube.com/watch?v=bSbvNI3ftXw&t=1323s"
transcription = transcribe_stream(url)
print(transcription)
