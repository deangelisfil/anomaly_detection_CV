import cv2

def convertFrame(im, resizeCoef, resize=True):
    # converts frame to grey, resizes image according to resizeCoef and smoothens
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    if resize:
        shape = im.shape
        im = cv2.resize(im, (shape[1]//resizeCoef, shape[0]//resizeCoef))
    im = cv2.GaussianBlur(im, (21, 21), 0)
    return im

def nextFrame(vs, resizeCoef, resize):
    # opens the next frame of vs and returns the converted frame
    success, frame = vs.read()
    frameG = convertFrame(frame, resizeCoef, resize)
    return frameG
