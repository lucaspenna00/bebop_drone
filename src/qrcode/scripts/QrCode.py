import rospy
import numpy as np
import cv2
import cv_bridge
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import pyzbar.pyzbar as pyzbar
from qrtools import QR
import gi


class QrCode:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/bebop/image_raw", Image, self.image_callback)

    def image_callback(self, image):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(image, "mono8")
            #self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.gray = self.cv_image
            self.detect()

        except CvBridgeError as e:
            print (e)

        cv2.waitKey(3)

    def detect(self):
        cv2.imshow("Camera", self.cv_image)
        decodedObject = self.decode(self.cv_image)
        self.display(self.cv_image, decodedObject)

    def decode(self, im):

        decodedObjects = pyzbar.decode(im)
 
        for obj in decodedObjects:

            f = open("Inventario.txt", "a")
            f.write(str(obj.data) + '\n')
            
            print('Type : ', obj.type)
            print('Data : ', obj.data,'\n')
         
        return decodedObjects

    def display(self, im, decodedObjects):

    	n = 0

    	for decodedObject in decodedObjects: 

	        points = decodedObject.polygon
	     
	        # If the points do not form a quad, find convex hull
	        if len(points) > 4 : 
	          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
	          hull = list(map(tuple, np.squeeze(hull)))
	        else : 
	          hull = points;
	         
	        # Number of points in the convex hull
	        n = len(hull)
	     
        # Draw the convext hull
        for j in range(0,n):

        	cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
     
     	 # Display results s
		cv2.imshow("Results", im)

def main():
    detecter = QrCode()
    rospy.init_node('QrCode', anonymous=True)
    rate = rospy.Rate(100)
    while True:
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print('Shutting Down')
    cv2.destroyAllWindows()
    rate.sleep()

if __name__ == "__main__":
    main()
