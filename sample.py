import cv2
import threading


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
    try:
         while True:
            frame = camera.get_frame()

           
            cv2.imshow("circles", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    except:  
        print('completed')
            
def cam1_start():
    value=cv2.VideoCapture('rtsp://admin:user@123@49.207.177.194:10554/Streaming/Channels/101')
    cam = PlayCamera(value)
    gen(cam)





  