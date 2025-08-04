
from video_utils import download_video, extract_frames, extract_audio
from  emotion_utils import detect_emotions_in_folder

if __name__ == "__main__":
    YOUTUBE_URL = "https://www.youtube.com/shorts/rI6OIwEOt1M"
    VIDEO_FILE = "video.mp4"

    # Step 1: Download video
    download_video(YOUTUBE_URL, VIDEO_FILE)

    # Step 2: Extract frames
    extract_frames(VIDEO_FILE, fps=1)

    # Step 3: Extract audio
    extract_audio(VIDEO_FILE)

    # Step 4: Emotion Detection from Frames
    detect_emotions_in_folder("frames")

