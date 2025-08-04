import json

def combine_emotion_and_sentiment(emotion_file, sentiment_file, output_file):
    # Load emotion data (frame_0001.jpg: happy)
    with open(emotion_file, "r") as f:
        emotion_lines = f.readlines()
    
    # Map second → emotion (assuming 1 frame per second as per extract_frames)
    second_to_emotion = {}
    for idx, line in enumerate(emotion_lines):
        try:
            frame_name, emotion = line.strip().split(":")
            second_to_emotion[idx] = emotion.strip()
        except ValueError:
            continue

    # Load sentiment segments
    with open(sentiment_file, "r") as f:
        sentiment_segments = json.load(f)

    # Combine
    combined = []
    for seg in sentiment_segments:
        start_sec = int(seg["start"])
        emotion = second_to_emotion.get(start_sec, "neutral")

        combined.append({
            **seg,
            "emotion": emotion
        })

    # Save combined output
    with open(output_file, "w") as f:
        json.dump(combined, f, indent=2)

    print(f"[✓] Combined emotion + sentiment saved to {output_file}")
