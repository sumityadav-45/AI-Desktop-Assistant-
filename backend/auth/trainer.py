import cv2
import numpy as np
from PIL import Image  # pillow package
import os

# Path where face samples are stored
path = 'backend\\auth\\samples'

# Create recognizer and load Haar Cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier('backend\\auth\\haarcascade_frontalface_default.xml')

def Images_And_Labels(path):
    # Only include files (skip directories)
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)
                  if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        try:
            # Convert to grayscale
            gray_img = Image.open(imagePath).convert('L')
            img_arr = np.array(gray_img, 'uint8')

            # Extract ID from filename: assume format like User.1.jpg
            id = int(os.path.split(imagePath)[-1].split(".")[1])

            faces = detector.detectMultiScale(img_arr)

            for (x, y, w, h) in faces:
                faceSamples.append(img_arr[y:y+h, x:x+w])
                ids.append(id)

        except Exception as e:
            print(f"Skipping file {imagePath}, error: {e}")
    
    return faceSamples, ids

print("Training faces. It will take a few seconds. Wait ...")

faces, ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

# Make sure trainer folder exists
trainer_dir = 'backend\\auth\\trainer'
if not os.path.exists(trainer_dir):
    os.makedirs(trainer_dir)

recognizer.write(os.path.join(trainer_dir, 'trainer.yml'))

print("Model trained, now we can recognize your face.")
