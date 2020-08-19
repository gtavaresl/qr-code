# import the necessary packages
from __future__ import print_function
from QRmission.QRdecode import QRdecode
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS
import argparse
import cv2
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m","--mode", default = int(0), help = "mode of operation")
ap.add_argument("-i", "--input", default = int(0), help = "path to input")
ap.add_argument("-o", "--output", default = int(0), help ="path to output")
args = vars(ap.parse_args())

qr = QRdecode()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
if args["mode"] == 0:
	vs = WebcamVideoStream(args["input"]).start()
	time.sleep(2.0)
else:
	vs = FileVideoStream(args["input"]).start()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

resolution = (1280, 720)
frame_rate = 20
rec = cv2.VideoWriter(args["output"], fourcc, frame_rate, resolution)

print("[INFO] THREADED frames initialized...")
fps = FPS().start()


# loop over some frames...this time using the threaded stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	try:
		#frame = cv2.resize(frame, (1280,960))#imutils.resize(frame, width = 640, height = 480)
		frame = qr.process(frame)
		# check to see if the frame should be displayed to our screen
		#cv2.imshow("Frame", frame)
		rec.write(frame)
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
rec.release()

qr.fwrite()
qr.fclose()