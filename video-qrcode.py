# import the necessary packages
from pyzbar import pyzbar
import cv2
import numpy as np
import time

videoName = "Passagem\Passagem 2 - Teste 3"

def qrcode(image, f, code):
    # find the barcodes in the image and decode each of the barcodes
    barcodes = pyzbar.decode(image)

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # print the barcode type and data to the terminal
        if(len(code) == 0 or code[len(code)-1] != barcodeData):
            f.write(barcodeData + '\n')
            code.append(barcodeData)
            cv2.imwrite(videoName + " - Image "+ str(len(code)) + ".png", frame)
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    # show the output image
    cv2.imshow("Image", image)
    #cv2.waitKey(0)

f = open("barcodes.txt","w")
code = []

cap = cv2.VideoCapture(videoName + ".mp4")
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
rec = cv2.VideoWriter("output.mp4", fourcc, 30, (1920, 1080))
#time.sleep(4.0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        #frame = cv2.resize(frame, (1280,960), interpolation = cv2.INTER_AREA)
        #cv2.imshow('Video Original',frame)
        qrcode(frame, f, code)
        rec.write(frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')) or ret == False:
        break

cap.release()
cv2.destroyAllWindows()

f.close()