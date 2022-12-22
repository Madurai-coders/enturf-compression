from django.shortcuts import render
from django.http import HttpResponse
import csv
import numpy
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import os
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import ffmpeg_streaming
import ffmpeg



# class VideoCamera(object):
#     def __init__(self):
#         print(cv2.getBuildInformation())
#         self.video = cv2.VideoCapture('static/Sunset.mp4')
#         # self.video = cv2.VideoCapture(0)
#         (self.grabbed, self.frame) = self.video.read()
#         # width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
#         # height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         self.fps = self.video.get(cv2.CAP_PROP_FPS)
       
        
#         threading.Thread(target=self.update, args=()).start()

#     def __del__(self):
#         self.video.release()
#         self.writer.release()

#     def get_frame(self):
#         image = self.frame
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         resize = cv2.resize(gray, (640, 480), interpolation=cv2.INTER_LINEAR)
#         imgBlur = cv2.GaussianBlur(resize, (7, 7), 1)
#         self.writer.write(resize)
#         ret, jpeg = cv2.imencode('.jpg', image)
#         # video = ffmpeg_streaming.input(jpeg.bytes(),capture=True)
#         # _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
#         # hls = video.hls(Formats.h264())
#         # hls.representations(_360p)
#         # hls.output('media/hls.m3u8')

#     def update(self):
#         for frame_idx in range(int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))):
#             (self.grabbed, self.frame) = self.video.read()
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break


# def gen(camera):
#     try:
#         while True:
#             frame = camera.get_frame()
#             yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#     except:
#         print('completed')


# # def playaswish(camera):
# #     try:
# #          while True:
# #             frame = camera.get_frame()
# #             yield (b'--frame\r\n'
# #                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
# #     except:
# #         print('completed')


# @gzip.gzip_page
# def livefe(request,):
#     try:
#         cam = VideoCamera()
#         while True:
#             cam.get_frame()
#     except:  # This is bad! replace it with proper handling
#           return HttpResponse('hi')

# @gzip.gzip_page
# def livefe(request,):
#     try:
#         cam = VideoCamera()
#         while True:
#             cam.get_frame()
#     except:  # This is bad! replace it with proper handling
#           return HttpResponse('hi')


# def index(request):
#     return render(request, 'streamapp/home.html')



# def gens():
#     video = cv2.VideoCapture('rtsp://admin:user@123@169.254.0.3:554/Streaming/Channels/101')
#     video.set(cv2.CAP_PROP_FPS, 25)
#     print("streaming live feed of ")
#     while True:
#         success, frame = video.read()  
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# def new(request): 
#         return StreamingHttpResponse(gens(),content_type="multipart/x-mixed-replace;boundary=frame")

# ------------------------------------------------------------------
class PlayCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('rtsp://admin:user@123@169.254.0.3:554/Streaming/Channels/101')
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
    def __del__(self):
        self.video.release()
    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        # hsl(jpeg.tobytes())
        return jpeg.tobytes()
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            cv2.waitKey(0)

def gen1(camera):
    try:
         while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    except:  # This is bad! replace it with proper handling
        print('completed')


@gzip.gzip_page
def Play(request,):
    try:
       cam = PlayCamera()
       return StreamingHttpResponse(gen1(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass



def hsl():
    cam = PlayCamera()
    play=StreamingHttpResponse(gen1(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    video = ffmpeg_streaming.input(play,capture=True)
    _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    hls = video.hls(Formats.h264())
    hls.representations(_360p)
    hls.output('media/hls.m3u8')
    return HttpResponse('hi')


