# USAGE

# import the necessary packages
import argparse
import numpy as np
import cv2
from datetime import datetime
import imutils
from imutils import build_montages
from imutils.video import FPS
from imagezmq import ImageHub
from QRpackage.QRdecode import QRdecoder

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())

# initialize the QRdecoder object
qr = QRdecoder()

# initialize the ImageHub object
imageHub = ImageHub()
print("[INFO] Server initialized...")

frameDict = {}

# initialize the dictionary which will contain  information regarding
# when a device was last active, then store the last time the check
# was made was now
lastActive = {}
lastActiveCheck = datetime.now()

# stores the estimated number of cameras, active checking period, and
# calculates the duration seconds to wait before making a check to
# see if a device was active
ESTIMATED_NUM_CAMS = 1
ACTIVE_CHECK_PERIOD = 10
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_CAMS * ACTIVE_CHECK_PERIOD

print("[INFO] Waiting for connections...")

fps = FPS().start()

# start looping over all the frames
while True:
    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    (rpiName, frame) = imageHub.recv_image()

    # if a device is not in the last active dictionary then it means
    # that its a newly connected device
    if rpiName not in lastActive.keys():
        print("[INFO] Receiving data from {}...".format(rpiName))

    # record the last active time for the device from which we just
    # received a frame
    lastActive[rpiName] = datetime.now()

    # detect any kepresses
    key = cv2.waitKey(1) & 0xFF

    if key == ord('f'):
        qr.setFilter(not qr.getFilter())

    # resize the frame to have a maximum width of 400 pixels, then
    # grab the frame dimensions and construct a blob
    frame = imutils.resize(frame, width=400)
    (h, w) = frame.shape[:2]

    frame, qrcodeData = qr.process(frame)
    
    # reply to client
    if qrcodeData is not None:
        imageHub.send_reply(bytes(qrcodeData, 'utf-8'))
    else:
        imageHub.send_reply(b'[INFO] QR Code not found')

    # draw if the filter is on
    cv2.putText(frame, "Filter: " + str(qr.getFilter()), (5, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # draw the sending device name on the frame
    cv2.putText(frame, rpiName, (5, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # update the new frame in the frame dictionary
    frameDict[rpiName] = frame
    cv2.imshow("Frame", frame)

    # if current time *minus* last time when the active device check
    # was made is greater than the threshold set then do a check
    if (datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
        # loop over all previously active devices
        for (rpiName, ts) in list(lastActive.items()):
            # remove the RPi from the last active and frame
            # dictionaries if the device hasn't been active recently
            if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
                print("[INFO] lost connection to {}".format(rpiName))
                lastActive.pop(rpiName)
                frameDict.pop(rpiName)

        # set the last active check time as current time
        lastActiveCheck = datetime.now()

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        (rpiName, frame) = imageHub.recv_image()
        imageHub.send_reply(b'Server disconnected')
        break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
