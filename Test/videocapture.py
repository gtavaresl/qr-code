import cv2
import time


outName = input("outputName: ")

cap = cv2.VideoCapture(0)
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#rec = cv2.VideoWriter("output.avi", fourcc,17 , (640, 480))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
rec = cv2.VideoWriter(outName + ".mp4", fourcc, 30, (640, 480))
time.sleep(4.0)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        #cv2.imshow('Video Original',frame)
        print("Recording...")
        rec.write(frame)
    print(cap.get(cv2.CAP_PROP_FPS))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()