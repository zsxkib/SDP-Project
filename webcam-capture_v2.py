import cv2 
import time
import numpy as np
from io import BytesIO
import requests

key = cv2.waitKey(1)
key2 = cv2.waitKey(1)
webcam = cv2.VideoCapture(0)
webcam2 = cv2.VideoCapture(1)
while True:
    try:
        check, frame = webcam.read()
        check2, frame2 = webcam2.read()
        # print(check) #prints true as long as the webcam is running
        # print(frame) #prints matrix values of each framecd 
        
        
        #cv2.imshow("Capturing", frame)
        #cv2.imshow("Capturing", frame2)
        # print(np.shape(frame))
        # print(np.array(frame))
        numpyarray = np.array(frame)
        numpyarray2 = np.array(frame2)
        f = BytesIO()
        np.savez_compressed(f, image_top = numpyarray, image_side = numpyarray2)
        res = requests.post('http://localhost:5000/classify', data = f.getvalue())
        print(res.content)

        key = cv2.waitKey(1)


        ## the next step will be to get the output from the classifier
        ##and then tell the car which bin to go to.

      
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
    