# import the necessary packages
import argparse
import time
import imutils
import cv2
from QRpackage.QRdecode import QRdecoder

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="input image filename")
ap.add_argument("-o", "--output", required=False,
                default=None, help="output image filename")
ap.add_argument("-t", "--txt", required=False,
                default=None, help="output txt filename")
ap.add_argument("-f", "--file", required=False, default=None,
                help="path to output file txt")
args = vars(ap.parse_args())

# create the object decoder
qr = QRdecoder(args["txt"], filter=True)


# read the image
image = cv2.imread("../images/input/" + args["input"])

# resize to a default resolution
resolution = (640, 480)
image = cv2.resize(image, resolution)

# process and show
processed, dataQRCode = qr.process(image)

cv2.imshow("Processed Image", processed)

cv2.waitKey(0)

# saves the output image
if args["output"]:
    cv2.imwrite("../images/output/" + args["output"], processed)
    print("[INFO] Saving {} at ../images/output/".format(args["output"]))


cv2.destroyAllWindows()

if args["file"] is not None:
    qr.fwrite()
    qr.fclose()
