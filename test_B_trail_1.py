import subprocess
import cv2
import threading
import numpy as np
import imutils
import multiprocessing

fps = 30
width = 400
height = 800

command1 = ['ffmpeg',
        '-y',
        '-re',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "{}x{}".format(width, height),
        '-r', str(fps),
        '-i', '-',
        '-pix_fmt', 'yuv420p',
        '-r', '30',
        '-g', '50',
        '-c:v', 'libx264',
        '-b:v', '2M',
        '-bufsize', '64M',
        '-maxrate', "4M",
        '-preset', 'veryfast',
        '-rtsp_transport', 'tcp',
        '-segment_times', '5',
        '-f', 'rtsp',
        'rtsp://65.1.134.231:8554/mystream',
        # '-start_number','0',
        # '-hls_time','1',
        # '-hls_list_size','0',
        # '-f','hls',
        # r'C:\Users\Kaamil\Documents\enturf-compression\media\cam1\hsl.m3u8'
        ]

# command2 = ['ffmpeg',
#         '-y',
#         '-re',
#         '-f', 'rawvideo',
#         '-vcodec', 'rawvideo',
#         '-pix_fmt', 'bgr24',
#         '-s', "{}x{}".format(width, height),
#         '-r', str(fps),
#         '-i', '-',
#         '-pix_fmt', 'yuv420p',
#         '-r', '30',
#         '-g', '50',
#         '-c:v', 'libx264',
#         '-b:v', '2M',
#         '-bufsize', '64M',
#         '-maxrate', "4M",
#         '-preset', 'veryfast',
#         '-rtsp_transport', 'tcp',
#         '-segment_times', '5',
#         '-f', 'rtsp',
#         'rtsp://localhost:8554/mystream2',
#         # '-start_number','0',
#         # '-hls_time','1',
#         # '-hls_list_size','0',
#         # '-f','hls',
#         # r'C:\Users\Kaamil\Documents\enturf-compression\media\cam2\hsl'
#         ]

p1 = subprocess.Popen(command1, stdin=subprocess.PIPE)
# p2 = subprocess.Popen(command2, stdin=subprocess.PIPE)



class PlayCamera(object):
    def __init__(self,value):
        self.video = value
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

def gen(camera,p):
         greenLower = (29, 86, 6)
         greenUpper = (64, 255, 255)
        #  greenLower = (0, 166, 0)
        #  greenUpper = (25, 255, 255)
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

            # cv2.imshow("circles", resize)

            p.stdin.write(resize.tobytes())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            

            
def cam1_start():
    value=cv2.VideoCapture('rtsp://admin:user@123@49.207.177.194:10554/Streaming/Channels/101')
    cam = PlayCamera(value)
    gen(cam,p1)


# def cam2_start():
#     value=cv2.VideoCapture('rtsp://admin:user@123@169.254.17.246:554/Streaming/Channels/101')
#     cam = PlayCamera(value)
#     gen(cam,p2)

# cam1_start()
# cam2_start()

# if __name__ == '__main__':

#     threading(target = cam1_start).start()
#     threading(target = cam2_start).start()
#     while True:
#         time.sleep(5)


if __name__ == "__main__":
    # creating processes
    p1 = multiprocessing.Process(target=cam1_start, args=())
    # p2 = multiprocessing.Process(target=cam2_start, args=( ))

    p1.start()
    # p2.start()
  