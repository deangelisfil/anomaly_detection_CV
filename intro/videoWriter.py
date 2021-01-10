import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
ret, background = cap.read()
print(ret, background.shape)
capSize = (background.shape[1], background.shape[0]) # this is the size of my SOURCE video. If the sizes do not match, no video is written.
# attention: img.shape gives (height, width, dim), while we are interested in (width height)
fs = 20
out = cv2.VideoWriter('outputSample.avi',fourcc, fs, capSize, True)

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame, 0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()