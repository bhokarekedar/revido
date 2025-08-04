from fer import FER
import cv2

img_path = "/Users/kedarbhokare/Desktop/pythonlessons/reactionvideo/sample.jpg"
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"Image not found at: {img_path}")

detector = FER(mtcnn=True)
emotion = detector.detect_emotions(img)
print(emotion)
