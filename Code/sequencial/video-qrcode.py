# import the necessary packages
from QRmission.QRdecode import QRdecode
import cv2
import numpy as np
import time
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", default = int(0), help = "path to input video")
ap.add_argument("-o", "--output", default = "output", help = "path to output video")
ap.add_argument("-f", "--file", default = "barcodes", help = "path to output file txt")
args = vars(ap.parse_args())

qr = QRdecode(args["file"])

if(args["input"] == 0):
    cap = cv2.VideoCapture(0)
    args["input"] = "Webcam"
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    args["output"] += ".avi"

else:
    cap = cv2.VideoCapture(args["input"])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    args["output"] += ".mp4"

resolution = (1920, 1080)
frame_rate = 30

rec = cv2.VideoWriter(args["output"], fourcc, frame_rate, resolution)


while(True):
    # Capture frame-by-frame
    grabbed, frame = cap.read()
    if grabbed == True:
        frame = qr.process(frame)
        cv2.imshow('Frame',frame)
        rec.write(frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')) or not grabbed:
        break

cap.release()
rec.release()
cv2.destroyAllWindows()

qr.fwrite()
qr.fclose()