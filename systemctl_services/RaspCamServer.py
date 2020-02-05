#!/usr/bin/python3

from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import cv2
from PIL import Image, ImageOps
import time

from picamera import PiCamera

global camera
camera = PiCamera()
camera.resolution = (1296, 972)
camera.hflip = True
global proporcao
proporcao = 5
camera.start_preview(fullscreen=False,window=(1350,150,int(camera.resolution[0]/proporcao),int(camera.resolution[1]/proporcao)))

def TakePicture():
    print("1")
    global camera
    camera.close()
    try:
        video_capture = cv2.VideoCapture(0)
        print("2")
        ret, frame = video_capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(frame)
        im_pil = ImageOps.mirror(im_pil)
        im_pil.save("/home/pi/socketcam/imagem01.jpg")
        print("ate aqui ok")
        cv2.destroyAllWindows()
        video_capture.release()       
        
        with open("/home/pi/socketcam/imagem01.jpg", "rb") as handle:
            return xmlrpc.client.Binary(handle.read())

    except Exception as e:
        print(e)
        return 0
    finally:
        camera = PiCamera()
        camera.resolution = (1296, 972)
        camera.hflip = True
        proporcao = 5
        camera.start_preview(fullscreen=False,window=(1350,150,int(camera.resolution[0]/proporcao),int(camera.resolution[1]/proporcao)))

server = SimpleXMLRPCServer(("192.168.100.28", 8000))
print("Listening on port 8000...")
server.register_function(TakePicture, 'TakePicture')

server.serve_forever()

