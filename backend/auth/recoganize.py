import cv2
import time
import pyautogui as p

def AuthenticateFace():
    # Load trained recognizer and Haar cascade
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('backend\\auth\\trainer\\trainer.yml')
    faceCascade = cv2.CascadeClassifier('backend\\auth\\haarcascade_frontalface_default.xml')

    # Font and ID mapping
    font = cv2.FONT_HERSHEY_SIMPLEX
    names = ['', '', 'Sumit']  # Add names at indices matching label IDs in training

    # Initialize webcam
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # Width
    cam.set(4, 480)  # Height

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    flag = 0  # 1 if authenticated, 0 otherwise

    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            label_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 100:
                name = names[label_id] if label_id < len(names) else "Unknown"
                confidence_display = f"  {round(100 - confidence)}%"
                flag = 1
            else:
                name = "Unknown"
                confidence_display = f"  {round(100 - confidence)}%"
                flag = 0

            cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, confidence_display, (x+5, y+h-5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        key = cv2.waitKey(10) & 0xff
        if key == 27 or flag == 1:  # Exit on ESC or successful recognition
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag
