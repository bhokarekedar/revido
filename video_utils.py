# video_utils.py

import os
import subprocess

def download_video(youtube_url: str, output_path: str = "video.mp4"):
    """Downloads the YouTube video and merges best video + audio using yt-dlp."""
    command = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio",
        "--merge-output-format", "mp4",
        "-o", output_path,
        youtube_url
    ]
    subprocess.run(command, check=True)
    print(f"[✓] Downloaded and saved video to {output_path}")

def extract_frames(video_path: str, output_dir: str = "frames", fps: int = 1):
    """Extracts frames from video at given FPS."""
    os.makedirs(output_dir, exist_ok=True)
    output_pattern = os.path.join(output_dir, "frame_%04d.jpg")
    command = [
        "ffmpeg", "-i", video_path,
        "-vf", f"fps={fps}",
        output_pattern
    ]
    subprocess.run(command, check=True)
    print(f"[✓] Extracted frames to {output_dir}/")

def extract_audio(video_path: str, output_path: str = "audio/audio.wav"):
    """Extracts audio from video."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    command = [
        "ffmpeg", "-i", video_path,
        "-q:a", "0", "-map", "a", output_path
    ]
    subprocess.run(command, check=True)
    print(f"[✓] Extracted audio to {output_path}")
