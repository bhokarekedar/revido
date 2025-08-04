import os
import cv2
from fer import FER

def detect_emotions_in_folder(frame_folder: str, output_file: str = "outputs/emotions_summary.txt"):
    detector = FER()
    results = []

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for file_name in sorted(os.listdir(frame_folder)):
        if file_name.endswith(".jpg"):
            frame_path = os.path.join(frame_folder, file_name)
            img = cv2.imread(frame_path)

            if img is None:
                continue

            # Detect emotion
            emotion, score = detector.top_emotion(img)

            if emotion is not None and score is not None:
                results.append((file_name, emotion, score))
                print(f"{file_name}: {emotion} ({score:.2f})")
            else:
                print(f"{file_name}: No emotion detected")

    # Save results to a text file
    with open(output_file, "w") as f:
        for file_name, emotion, score in results:
            f.write(f"{file_name}: {emotion} ({score:.2f})\n")

    print(f"[✓] Emotion analysis complete. Results saved to {output_file}")
