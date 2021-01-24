import cv2
from parameters import *
("Package imported")

img = cv2.imread( str(pathImage) )
cv2.imshow("Output", img)
cv2.waitKey(0)

cap = cv2.VideoCapture( str(pathVideo) )
while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

