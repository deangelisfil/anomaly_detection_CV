import cv2
import numpy as np
import imutils
from parameters import *
from utilityFunctions import *

# We follow the approach in
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# To do: set time-dependent background

if vsPath == "":
    # set computer camera as video stream
    vs = cv2.VideoCapture(0)
else:
    vs = cv2.VideoCapture(vsPath)

if backgroundPath == "":
    # if no background, use first frame as background
    success, frame = vs.read()
    frameG = resizeFrame(frame, resizeCoef)
    background = frameG
else:
    background = cv2.imread(backgroundPath)
    background = resizeFrame(background, resizeCoef)

fps = vs.get(cv2.CAP_PROP_FPS)
# recall height, width, channels = img.shape
capSize = (background.shape[1], background.shape[0])
# capSize = (vs.get(cv2.CAP_PROP_FRAME_WIDTH), vs.get(cv2.CAP_PROP_FRAME_HEIGHT)) # can not be used, since I'll resize caption
fourcc = cv2.VideoWriter_fourcc(*'MPEG') # four character code, determines the video codec with which the video will be compressed
out = cv2.VideoWriter(outPath, fourcc, fps, capSize, False)

while vs.isOpened():
    success, frame = vs.read()
    frameG = resizeFrame(frame, resizeCoef)

    frameDelta = cv2.absdiff(background, frameG)
    frameThresh = cv2.threshold(frameDelta, minBackgroundDiff, 255, cv2.THRESH_BINARY)[1]

    # Dilation and then grab contours
    frameThresh = cv2.dilate(frameThresh, None, iterations=2)
    cnts = cv2.findContours(frameThresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) > minAreaContour:
            # compute the bounding box for the contour, draw it on the frame
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frameG, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    out.write(frameG)
    cv2.imshow("frameG", frameG)
    cv2.imshow("frameDelta", frameDelta)
    cv2.imshow("frameThresh", frameThresh)

vs.release()
cv2.destroyAllWindows()
