import cv2

def resizeFrame(im, resizeCoef):
    # converts frame to grey, resizes image according to resizeCoef and smoothens
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    shape = im.shape
    im = cv2.resize(im, (shape[1]//resizeCoef, shape[0]//resizeCoef))
    im = cv2.GaussianBlur(im, (21, 21), 0)
    return im
