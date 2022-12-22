import subprocess
import cv2
import threading
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import numpy as np
import imutils
import ffmpeg_streaming
import time
import multiprocessing


class PlayCamera(object):
    def __init__(self,value):
        self.video = value
        fps = self.video.get(cv2.CAP_PROP_FPS)
        print(fps)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
    def __del__(self):
        self.video.release()
    def get_frame(self):
        image = self.frame
        return image
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            cv2.waitKey(100)
  



def gen(camera):
    try:
         greenLower = (0, 166, 0)
         greenUpper = (25, 255, 255)
         while True:
            frame = camera.get_frame()
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
                            (0, 255, 255), 0.1)
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
    
            resize=cv2.resize(cropped_image,(400,800))

            cv2.imshow("circles", resize)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    except:   
        print('completed')


def cam1_start():
    value=cv2.VideoCapture('static/sample1.mp4')
    cam = PlayCamera(value)
    gen(cam)

cam1_start()
