import cv2
import numpy as np
from parameters import *

print(os.getcwd())
img = cv2.imread(str(pathImage))
print(pathImage)
cv2.imshow("Output", img)

# convert to grey scale
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #note that cv2 is stored in BGR2 not in RGB
cv2.imshow("OutputGrey", imgGrey)

# edge detector canny
imgCanny = cv2.Canny(img, 120,200)
cv2.imshow("OutputEdges", imgCanny)

# Dilation
kernel = np.ones((5,5),np.uint8)
imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)
cv2.imshow("OutputDilation", imgDilation)


cv2.waitKey(0)


