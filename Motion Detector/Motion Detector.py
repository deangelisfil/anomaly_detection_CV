import cv2
import numpy as np
import imutils

# We follow the approach in
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# Parameters
resizeCoef = 3
vsPath = "../Resources/sorpasso.mp4"
backgroundPath = "../Resources/background.jpg"
minAreaContour = 800
minBackgroundDiff = 125

# utility functions
def resizeFrame(im, resizeCoef):
    # converts to grey, resizes image according to resizeCoef and smoothens
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    shape = im.shape
    im = cv2.resize(im, (shape[1]//resizeCoef, shape[0]//resizeCoef))
    im = cv2.GaussianBlur(im, (21, 21), 0)
    return im


# Motion Detector
vs = cv2.VideoCapture(vsPath)
background = cv2.imread(backgroundPath)
background = resizeFrame(background, resizeCoef)

while True:
    success, frame = vs.read()
    frameG = resizeFrame(frame, resizeCoef)

    # if no background, use first frame as background
    if background is None:
        background = frameG

    frameDelta = cv2.absdiff(background, frameG)
    frameThresh = cv2.threshold(frameDelta, minBackgroundDiff, 255, cv2.THRESH_BINARY)[1]

    frameThresh = cv2.dilate(frameThresh, None, iterations=2)
    cnts = cv2.findContours(frameThresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) > minAreaContour:
            # compute the bounding box for the contour, draw it on the frame
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frameG, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if frame is None or (cv2.waitKey(1) & 0xFF == ord("q")):
        break

    cv2.imshow("frameG", frameG)
    cv2.imshow("frameDelta", frameDelta)
    cv2.imshow("frameThresh", frameThresh)


