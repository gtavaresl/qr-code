# import the necessary packages
from QRmission.QRdecode import QRdecode
import cv2
import argparse
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS
import time


'''
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", default = int(0), help = "path to input video")
ap.add_argument("-o", "--output", default = "output", help = "path to output video")
ap.add_argument("-f", "--file", default = "barcodes", help = "path to output file txt")
args = vars(ap.parse_args())


if(args["input"] == 0):
    args["input"] = "Webcam"
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    args["output"] += ".avi"

else:
    cap = cv2.VideoCapture(args["input"])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    args["output"] += ".mp4"
'''
qr = QRdecode()
vs = WebcamVideoStream(0).start()

time.sleep(2.0)

resolution = (640, 360)
frame_rate = 25

#rec = cv2.VideoWriter(args["output"], fourcc, frame_rate, resolution)

print("[INFO] THREADED frames initialized...")
fps = FPS().start()

while True:
    # grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	try:
		frame = imutils.resize(frame, width = 640, height = 480)
		frame = qr.process(frame)
		# check to see if the frame should be displayed to our screen
		cv2.imshow("Frame", frame)
		#rec.write(frame)
		# update the FPS counter
		fps.update()
	except cv2.error as e:
		print("[INFO] client disconnected!")
		break
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# stop the timer and display FPS information
fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

qr.fwrite()
qr.fclose()