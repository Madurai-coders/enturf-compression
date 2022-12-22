import subprocess
import cv2
import threading
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import numpy as np
import imutils

rtmp_url = "rtmp://127.0.0.1:1935/live/test"
cap = cv2.VideoCapture('rtsp://admin:user@123@169.254.0.3:554/Streaming/Channels/101')
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = 400
height = 800

command = ['ffmpeg',
           '-y',
           '-re',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'libx264',
           '-preset', 'ultrafast',
   
           '-f', 'flv',
           rtmp_url]

p = subprocess.Popen(command, stdin=subprocess.PIPE)


class PlayCamera(object):
    def __init__(self,value):
        self.video = cap
       
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

def gen(camera):
    try:

         greenLower = (29, 86, 6)
         greenUpper = (64, 255, 255)
         while True:
            frame = camera.get_frame()
            frame = imutils.resize(frame, width=600)
            # frame = cv2.UMat(frame)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # hsv= cv2.UMat.get(hsv)
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
    
            resize=cv2.resize(cropped_image,(400,800))
            cv2.imshow("circles", resize)
            p.stdin.write(resize.tobytes())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    except:  
        print('completed')
            

cam = PlayCamera()
gen(cam)
