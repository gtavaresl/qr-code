# import the necessary packages
import argparse
import cv2
from pyzbar import pyzbar

# implements a class QRdecoder


class QRdecoder:
    def __init__(self, fileName=None, range=200, filter=False):
        # create a file to save the list of qrcodes
        if fileName is not None:
            try:
                self.file = open(fileName + ".txt", "w")
                print("[INFO] File {}.txt created".format(fileName))
            except:
                print("[INFO] Can't create {}.txt file".format(fileName))
        # list of qrcodes
        self.code = []
        # range of threshold filter
        self.range = range
        # boolean ON/OFF filter
        self.filter = filter

    def filter_operations(self, image):
        # Applies a threshold filter
        image = cv2.inRange(
            image, (0, 0, 0), (self.range, self.range, self.range))
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        #image = cv2.blur(image, (9, 9))
        image = 255 - image  # black-in-white

        # perform a series of erosions and dilations
        #image = cv2.erode(image, None, iterations = 1)
        #image = cv2.dilate(image, None, iterations = 1)
        return image

    def setFilter(self, newFilter):
        self.filter = newFilter

    def getFilter(self):
        return self.filter

    def process(self, image):
        # if filter is on, apply at image
        image = self.filter_operations(image) if self.filter == True else image

        # find the qrcodes in the image and decode each of the qrcodes
        qrcodes = pyzbar.decode(image, symbols=[pyzbar.ZBarSymbol.QRCODE])

        # to be returned if found a qrcode
        qrcodeData = []

        # loop over the detected qrcodes
        for qrcode in qrcodes:
            # extract the bounding box location of the qrcode and draw the
            # bounding box surrounding the qrcode on the image
            (x, y, w, h) = qrcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the qrcode data is a bytes object so if we want to draw it on
            # our output image we need to convert it to a string first
            qrcodeData = qrcode.data.decode("utf-8")
            qrcodeType = qrcode.type
            # draw the qrcode data and qrcode type on the image
            text = "{} ({})".format(qrcodeData, qrcodeType)
            cv2.putText(image, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # print the qrcode type and data to the terminal
            if qrcodeData not in self.code:
                self.code.append(qrcodeData)
                print("[INFO] Found QRCODE: " + qrcodeData)

        return image, qrcodeData

    def fwrite(self):
        for qrcodeData in self.code:
            self.file.write(qrcodeData + '\n')

    def fclose(self):
        self.file.close()
