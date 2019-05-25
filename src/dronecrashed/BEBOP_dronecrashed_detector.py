from keras.preprocessing.image import img_to_array
from keras.models import load_model
import keras
import numpy as np
import cv2
import cv_bridge
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import rospy

MODEL_PATH = "dronecrashednotcrashed.model"

class MAVCrashed:

    def __init__(self):

        self.bridge = CvBridge()

        self.image_sub = rospy.Subscriber("/bebop/image_raw", Image, self.image_callback)

    def image_callback(self, image):

        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(image)

            self.detect_crashed_mav()

        except CvBridgeError as e:
            print(e)

        cv2.waitKey(3)


    def detect_crashed_mav(self):

        cv2.imshow("BEBOP CAMERA", self.cv_image)
        model = load_model(MODEL_PATH)
        frame = self.cv_image
        self.cv_image = cv2.resize(self.cv_image, (28, 28))
        self.cv_image = self.cv_image.astype("float") / 255.0
        self.cv_image = img_to_array(self.cv_image)
        self.cv_image = np.expand_dims(self.cv_image, axis=0)
        (notCrashed, crashed) = model.predict(self.cv_image)[0]
        label = "Not Crashed"
        proba = notCrashed

        if crashed > notCrashed:

            label = "Crashed"
            proba = crashed

        label = "{}: {:.2f}%".format(label, proba * 100 )
        frame = cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('frame', frame)


def main():

    detectCrashed = MAVCrashed()
    rospy.init_node("MAV CRASHED CLASSIFIER", anonymous=True)
    rate = rospy.Rate(10000)

    while True:

        try:

            rospy.spin()

        except KeyboardInterrupt:

            print("Shutting Down")

    cv2.destroyAllWindows()
    rate.sleep()

if __name__ == "__main__":

    main()
