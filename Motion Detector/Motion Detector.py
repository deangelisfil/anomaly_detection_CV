import cv2
import numpy as np
import imutils

# Parameters
resizeCoef = 3
vsPath = "../Resources/sorpasso.mp4"
backgroundPath = "../Resources/background.jpg"

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

    if frame is None or (cv2.waitKey(1) & 0xFF == ord("q")):
        break

    # assume first frame is the background
    frameDelta = cv2.absdiff(background, frameG)
    frameDelta = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    cv2.imshow("Video", frameDelta)


    # next step is following the code/ approach in
    # https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/