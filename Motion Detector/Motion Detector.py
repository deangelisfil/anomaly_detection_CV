import cv2
import numpy as np

vs = cv2.VideoCapture("..\Resources\sorpasso.mp4")
while True:
    success, frame = vs.read()
    frameG = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    shape = frameG.shape
    frameG = cv2.resize(frameG, (shape[1]//3, shape[0]//3))
    # frameG = cv2.GaussianBlur(frameG, (21, 21), 0)

    cv2.imshow("Video", frameG)
    if frame is None or (cv2.waitKey(1) & 0xFF == ord("q")):
        break

    # next step is following the code/ approach in
    # https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/