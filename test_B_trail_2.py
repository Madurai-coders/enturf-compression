import subprocess
import cv2
import threading
import numpy as np
import imutils
import multiprocessing
import mediapipe as mp
import time


import websocket
import _thread
import time
import rel
import json

def on_message(ws, message):
    print(message)
    res = json.loads(message)
    print(res["type"])

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

    
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

def gen(camera):
         websocket.enableTrace(True)
         ws = websocket.WebSocketApp("ws://65.1.134.231:8001/ws/iot/",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
         ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        #  rel.signal(2, rel.abort)  # Keyboard Interrupt
         mpHands = mp.solutions.hands
         hands = mpHands.Hands()
         mpDraw = mp.solutions.drawing_utils
         pTime = 0
         cTime = 0
         id4=[]
         id8=[]
         while True:
            img = camera.get_frame()

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
 
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        # print(id, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        if id == 4:
                            # print(id, cx, cy)
                            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                            id4=[id, cx, cy]
                        if id == 8:
                            # print(id, cx, cy)
                            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                            id8=[id, cx, cy]

                            # if id4[1]-id8[1] < 10  and id4[2]-id8[2] < 10:
                            #     count = count+1
                            #     print(count)
                            #     if count > 50:
                            #         print('hi')
                            #         count = 0
                            
                                
                            # ws.send("Hello, World")

  
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
 
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
 
            cv2.imshow("circles", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                      
def cam1_start():
    value=cv2.VideoCapture(0)
    cam = PlayCamera(value)
    gen(cam)
    


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=cam1_start, args=())
    p1.start()







  

