
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time


greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

vs = VideoStream(
    'rtsp://admin:user@123@169.254.0.3:554/Streaming/Channels/101').start()


time.sleep(2.0)

while True:
   
    frame = vs.read()

    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 5:

            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    if center:
        start_val=center[0]-100
        End_val=center[0]+100
        if start_val<0:
             End_val=End_val-start_val
             start_val=0
        if End_val>600:
            start_val=start_val-End_val
            End_val=600
        cropped_image=frame[0:,start_val:End_val]
    else:
        cropped_image=frame[0:,200:400]
    


    cv2.imshow("Frame", cropped_image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()