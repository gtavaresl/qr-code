# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2

class QRdecode():
	def __init__(self, fileName = "barcodes", range = 200):
		self.file = open(fileName + ".txt","w")
		self.code = []
		self.range = range
	
	def process(self, image):
		# Filtro threshold
		image = cv2.inRange(image,(0,0,0),(self.range,self.range,self.range))
		image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
		#image = cv2.blur(image, (9, 9))
		image = 255 - image # black-in-white
		
		# perform a series of erosions and dilations
		#image = cv2.erode(image, None, iterations = 1)
		#image = cv2.dilate(image, None, iterations = 1)
		
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
			if(len(self.code) == 0 or self.code[len(self.code)-1] != barcodeData):
				self.code.append(barcodeData)
				print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

		# show the output image
		# cv2.imshow("Image", image)
		return image
	
	def fwrite(self):
		for barcodeData in self.code:
			self.file.write(barcodeData + '\n')

	def fclose(self):
		self.file.close()