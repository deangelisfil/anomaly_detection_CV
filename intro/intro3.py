import cv2
from parameters import *

img = cv2.imread(str(pathImage))
print(img.shape)

imgResize = cv2.resize(img, (622,800)) # width first, then height
cv2.imshow("Output", img)
cv2.imshow("OutputResize", imgResize)
cv2.waitKey(0)