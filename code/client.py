# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages
import argparse
import socket
import time
import cv2
import imutils
from imutils.video import VideoStream
from imagezmq import ImageSender
from QRpackage.QRdecode import QRdecoder

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", default='192.168.0.108',
                help="ip address of the server to which the client will connect")
ap.add_argument("-c", "--camera-ip", default='https://192.168.0.110:8080/video',
                help="ip address of the camera to which the client will connect")
args = vars(ap.parse_args())

qrcode_list = []

print("[INFO] Connecting to server...")

# initialize the ImageSender object with the socket address of the
# server
sender = ImageSender(connect_to="tcp://{}:5555".format(
    args["server_ip"]))

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
print("[INFO] Connection established with " + rpiName)

vs = VideoStream(src=args["camera_ip"]).start()
time.sleep(2.0)

print("[INFO] Sending frames")

while True:
    # read the frame from the camera and send it to the server
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    reply = sender.send_image(msg=rpiName, image=frame)
    if reply == b'Server disconnected':
        print("[INFO] Server disconnected")
        break
    elif reply != b'[INFO] QR Code not found':
        # Found a QR Code
        qrcodeData = reply.decode("utf-8")
        if(len(qrcode_list) == 0 or qrcode_list[len(qrcode_list)-1] != qrcodeData):
            qrcode_list.append(qrcodeData)
            print("[INFO] Found QRCODE: " + qrcodeData)

vs.stop()
