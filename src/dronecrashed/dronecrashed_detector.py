from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import time
import cv2
import os

cap = cv2.VideoCapture(0)

MODEL_PATH = "dronecrashednotcrashed.model"

# load the model
print("[INFO] loading model...")
model = load_model(MODEL_PATH)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    image = cv2.resize(frame, (28, 28))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    (notCrashed, crashed) = model.predict(image)[0]
    label = 'Not Crashed'
    proba = notCrashed

    if crashed > notCrashed:

        label = "Crashed"
        proba = crashed

    # Display the resulting frame
    label = "{}: {:.2f}%".format(label, proba * 100 )
    frame = cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
