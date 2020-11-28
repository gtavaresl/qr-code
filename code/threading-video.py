# import the necessary packages
import argparse
import imutils
import cv2
import time
from QRpackage.QRdecode import QRdecoder
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", default=int(0), help="mode of operation")
ap.add_argument("-i", "--input", default=int(0), help="path to input")
ap.add_argument("-o", "--output", default=int(0), help="path to output")
ap.add_argument("-f", "--file", required=False, default=None,
                help="path to output file txt")
args = vars(ap.parse_args())

# initialize the QRdecoder object
qr = QRdecoder()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
if args["mode"] == 0:
    vs = WebcamVideoStream(args["input"]).start()
    time.sleep(2.0)
else:
    vs = FileVideoStream(args["input"]).start()

#fourcc = cv2.VideoWriter_fourcc(*'mp4v')

resolution = (640, 480)
frame_rate = 20
#rec = cv2.VideoWriter(args["output"], fourcc, frame_rate, resolution)

print("[INFO] THREADED frames initialized...")
fps = FPS().start()


# loop over some frames...this time using the threaded stream
while True:
    # grab the frame from the threaded video stream
    frame = vs.read()
    key = cv2.waitKey(1) & 0xFF
    try:
        if key == ord('f'):
            qr.setFilter(not qr.getFilter())
        frame, _ = qr.process(frame)
        cv2.putText(frame, "Filter: " + str(qr.getFilter()), (5, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)
        # rec.write(frame)
        # update the FPS counter
        fps.update()
    except cv2.error as e:
        print("[INFO] Client disconnected!")
        break
    if key == ord('q'):
        print("[INFO] Server disconnected!")
        break

# stop the timer and display FPS information
fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
# rec.release()

if args["file"] is not None:
    qr.fwrite()
    qr.fclose()
