# transcription_utils.py

import whisper

def transcribe_audio(audio_path: str, output_txt_path: str):
    model = whisper.load_model("small")  # You can also try "base", "medium", etc.
    result = model.transcribe(audio_path)

    with open(output_txt_path, "w") as f:
        f.write(result["text"])

    print(f"[✓] Transcription complete. Saved to {output_txt_path}")
