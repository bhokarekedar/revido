import os
from urllib.parse import urlparse, parse_qs

from combine_emotion_and_sentiment import combine_emotion_and_sentiment
from video_utils import download_video, extract_frames, extract_audio
from emotion_utils import detect_emotions_in_folder
from transcription_utils import transcribe_audio
from sentiment_utils import analyze_sentiments

from whisper import load_model
import json

def get_video_id(youtube_url):
    if "youtube.com" in youtube_url:
        parsed = urlparse(youtube_url)
        if "shorts" in parsed.path:
            return parsed.path.split("/")[-1]
        return parse_qs(parsed.query).get("v", [""])[0]
    elif "youtu.be" in youtube_url:
        return youtube_url.split("/")[-1]
    return "video"

if __name__ == "__main__":
    YOUTUBE_URL = "https://www.youtube.com/shorts/rI6OIwEOt1M"
    VIDEO_ID = get_video_id(YOUTUBE_URL)
    OUTPUT_DIR = f"outputs/{VIDEO_ID}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    VIDEO_FILE = os.path.join(OUTPUT_DIR, f"{VIDEO_ID}.mp4")
    FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames")
    AUDIO_FILE = os.path.join(OUTPUT_DIR, f"{VIDEO_ID}.mp3")
    EMOTION_FILE = os.path.join(OUTPUT_DIR, f"{VIDEO_ID}_emotions.txt")
    TRANSCRIPT_FILE = os.path.join(OUTPUT_DIR, f"{VIDEO_ID}_transcript.txt")
    SENTIMENT_FILE = os.path.join(OUTPUT_DIR, f"{VIDEO_ID}_sentiments.json")
    COMBINED_FILE = os.path.join(OUTPUT_DIR, f"{VIDEO_ID}_combined.json")

    # Step 1: Download video
    download_video(YOUTUBE_URL, VIDEO_FILE)

    # Step 2: Extract frames
    extract_frames(VIDEO_FILE, fps=1, output_folder=FRAMES_DIR)

    # Step 3: Extract audio
    extract_audio(VIDEO_FILE, output_audio_path=AUDIO_FILE)

    # Step 4: Emotion Detection from Frames
    detect_emotions_in_folder(FRAMES_DIR, output_file=EMOTION_FILE)

    # Step 5: Transcribe with Whisper
    whisper_model = load_model("base")
    result = whisper_model.transcribe(VIDEO_FILE)
    segments = result["segments"]

    # Save plain transcript
    with open(TRANSCRIPT_FILE, "w") as f:
        for seg in segments:
            f.write(f"{seg['text'].strip()}\n")

    # Step 6: Sentiment Analysis of each segment
    sentiment_data = analyze_sentiments(segments)
    with open(SENTIMENT_FILE, "w") as f:
        json.dump(sentiment_data, f, indent=2)

    print(f"[✓] Sentiment analysis complete. Saved to {SENTIMENT_FILE}")

    # Step 7: Combine Emotion + Sentiment
    combine_emotion_and_sentiment(EMOTION_FILE, SENTIMENT_FILE, COMBINED_FILE)

    print(f"[✓] Combined emotion and sentiment data saved to {COMBINED_FILE}")
