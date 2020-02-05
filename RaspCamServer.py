from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import cv2
from PIL import Image




def TakePicture():
    print("1")
    try:
        video_capture = cv2.VideoCapture(0)
        print("2")
        ret, frame = video_capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(frame)
        im_pil.save("imagem01.jpg")
        print("ate aqui ok")
        cv2.destroyAllWindows()
        video_capture.release()       
        
        with open("imagem01.jpg", "rb") as handle:
            return xmlrpc.client.Binary(handle.read())


    except Exception as e:
        print(e)
        return 0


VirtualMachineIP = "ENTER IP HERE"
server = SimpleXMLRPCServer((VirtualMachineIP, 8000))
#server = SimpleXMLRPCServer(("localhost", 8000))

print("Listening on port 8000...")
server.register_function(TakePicture, 'TakePicture')

server.serve_forever()

