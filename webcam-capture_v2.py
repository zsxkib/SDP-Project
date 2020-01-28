from io import BytesIO
import numpy as np
import requests
import time

def capture(webcam):
    _, frame = webcam.read()
    return np.array(frame)[..., ::-1]

print('setting up opencv (few seconds)...')
import cv2
key = cv2.waitKey(1)
webcam = cv2.VideoCapture('/dev/video0')
webcam2 = cv2.VideoCapture('/dev/video2')

while True:
    try:
        time1 = time.time()
        arr1 = capture(webcam)
        arr2 = capture(webcam2)
        f = BytesIO()
        np.savez_compressed(f, image_top = arr1, image_side = arr2)
        time2 = time.time()
        print('time', time2-time1)
        res = requests.post('http://localhost:5000/classify', data = f.getvalue())
        print(res.content)

        key = cv2.waitKey(1)
        input()


        ## the next step will be to get the output from the classifier
        ##and then tell the car which bin to go to.

      
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
    
