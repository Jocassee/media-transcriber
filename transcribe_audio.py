import os
import whisper
from tqdm import tqdm

model = whisper.load_model("small").to("cuda")

def transcribe_audio(audio_dir="audio", model_size="small", output_file="transcript.txt"):
    try:
        model = whisper.load_model(model_size)
        transcriptions = {}
        audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]

        with open(output_file, "w", encoding="utf-8") as f, tqdm(total=len(audio_files), desc="Transcribing", unit="file") as pbar:
            for file in audio_files:
                file_path = os.path.join(audio_dir, file)
                result = model.transcribe(file_path)
                transcriptions[file] = result["text"]
                
                # Write to file
                f.write(f"File: {file}\n")
                f.write(f"Transcript:\n{result['text']}\n\n")

                # Update progress bar
                pbar.update(1)

        return transcriptions
    except Exception as e:
        print(f"Error during transcription: {e}")
        return {}

transcribe_audio(audio_dir="audio", model_size="small")
