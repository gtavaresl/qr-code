# import the necessary packages
import argparse
import numpy as np
import time
import cv2
from imutils.video import FPS
from QRpackage.QRdecode import QRdecoder

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", default=int(0), help="path to input video")
ap.add_argument("-o", "--output", default="output",
                help="path to output video")
ap.add_argument("-f", "--file", required=False,
                help="path to output file txt")
args = vars(ap.parse_args())

qr = QRdecoder(args["file"])

if(args["input"] == 0):
    cap = cv2.VideoCapture(0)
    args["input"] = "Webcam"
    time.sleep(2.0)
    #fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    #args["output"] += ".avi"

else:
    cap = cv2.VideoCapture(args["input"])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    args["output"] += ".mp4"

resolution = (640, 480)

#frame_rate = 30
#rec = cv2.VideoWriter(args["output"], fourcc, frame_rate, resolution)

print("[INFO] Frames initialized...")
fps = FPS().start()

while(cap.isOpened()):
    # Capture frame-by-frame
    grabbed, frame = cap.read()

    # detect any kepresses
    key = cv2.waitKey(1) & 0xFF

    if grabbed == True:
        if key == ord('f'):
            qr.setFilter(not qr.getFilter())
        frame, _ = qr.process(frame)
        cv2.putText(frame, "Filter: " + str(qr.getFilter()), (5, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow('Frame', frame)
        # rec.write(frame)
        # update the FPS counter
        fps.update()
    if key == ord('q') or not grabbed:
        break

# stop the timer and display FPS information
fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cap.release()
# rec.release()
cv2.destroyAllWindows()

if args["file"] is not None:
    qr.fwrite()
    qr.fclose()
