# import the necessary packages
from __future__ import print_function
from QRmission.QRdecode import QRdecode
import argparse
import imutils
import cv2
import time

qr = QRdecode()

resolution = (1280, 720)

image = cv2.imread("8x.JPG")

# resize

image = cv2.resize(image,resolution)

processed = qr.process(image)

cv2.imshow("Teste", processed)

cv2.waitKey(0)

cv2.destroyAllWindows()