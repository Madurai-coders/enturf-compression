import subprocess
import cv2
import threading
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import numpy as np
import imutils
import cvzone
from cvzone.ColorModule import ColorFinder

rtmp_url = "rtmp://127.0.0.1:1935/mystream"

# path = 'rtsp://admin:user@123@169.254.0.3:554/Streaming/Channels/101'
# path = 'rtsp://admin:user@123@169.254.0.3:554/Streaming/Channels/101'

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
        #    '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
        #    '-flags', 'low_delay'
        #    ' -tune', 'zerolatency'
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
         filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
         dist = lambda x1, y1, x2, y2: (x1-x2)**2+(y1-y2)**2
         prevCircle=None
        #  myColorFinder = ColorFinder(True)
         greenLower = (29, 86, 6)
         greenUpper = (64, 255, 255)
         hsvVals = {'hmin': 10, 'smin': 55, 'vmin': 215, 'hmax': 42, 'smax': 255, 'vmax': 255}
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
    


            # cv2.imshow("Frame", cropped_image)





































            # imgColor ,mask = myColorFinder.update(frame,hsvVals)
            # imgStack = cvzone.stackImages([frame, imgColor], 2, 1)
            # cv2.imshow("circles", frame)

            # cropped_image = frame[0:2000,2000:3000]
            resize=cv2.resize(cropped_image,(400,800))



            # sharpen_img_1=cv2.filter2D(frame,-1,filter)
            # blur=cv2.blur(sharpen_img_1,(5,5))

            # grayFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # blurFrame=cv2.GaussianBlur(grayFrame,(17,17), 0)
       
            # circles=cv2.HoughCircles(blurFrame,cv2.HOUGH_GRADIENT,1.2,100,param1=100,param2=30,minRadius=75,maxRadius=400)
            # if circles is not None:
            #     circles = np.uint16(np.around(circles))
            #     for i in circles[0,:]:
            #         cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)



            # if circles is not None:
            #     circles = np.uint16(np.around(circles))
            #     chosen = None
            # for i in circles [0, :]:
            #     if chosen is None: 
            #         chosen = i
            #     if prevCircle is not None:
            #         if dist(chosen [0], chosen [1], prevCircle [0], prevCircle [1]) <= dist(i[0],i[1], prevCircle [0], prevCircle [1]):
            #             chosen = i
            # cv2.circle (frame, (chosen [0], chosen[1]), 1, (0,100,100), 3)
            # cv2.circle (frame, (chosen[0], chosen[1]), chosen [2], (255,0,255), 3)
            # prevCircle = chosen

            # frame = cv2.resize(frame, (0,0), fx=0.3, fy=0.3) 
            # width = frame.get(cv2.CAP_PROP_FRAME_WIDTH )


            # print(width)
            cv2.imshow("circles", resize)
            # cv2.imshow("circles", frame)

            p.stdin.write(resize.tobytes())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    except:  
        print('completed')
            

# def store():
#     print ("Hey u called me")
#     video = ffmpeg_streaming.input('rtmp://127.0.0.1:1935/live/test',capture=True)
#     _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
#     hls = video.hls(Formats.h264())
#     hls.representations(_360p)
#     hls.output('media/hls.m3u8')

# threading.Timer(15.0, store).start()
cam = PlayCamera('rtsp://admin:user@123@169.254.0.3:554/Streaming/Channels/101')
gen(cam)
