import subprocess
import cv2
import threading
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import numpy as np
import imutils
import cvzone
from cvzone.ColorModule import ColorFinder


class PlayCamera(object):
    def __init__(self,value):
        self.video = cv2.VideoCapture('static/sample1.mp4')
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
            cv2.waitKey(150) 

def gen(camera):
    try:
         myColorFinder = ColorFinder(True)
         hsvVals = {'hmin': 10, 'smin': 165, 'vmin': 0, 'hmax': 21, 'smax': 255, 'vmax': 255}
         while True:
            frame = camera.get_frame()
            frame = imutils.resize(frame, width=600)

            imgColor ,mask = myColorFinder.update(frame,hsvVals)
            imgStack = cvzone.stackImages([frame, imgColor], 2, 1)
            cv2.imshow("circles", imgStack)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    except:  
        print('completed')
            


cam = PlayCamera('rtsp://admin:user@123@169.254.0.3:554/Streaming/Channels/101')
gen(cam)
