import cv2
print("Package imported")

img = cv2.imread("../Resources/Machiavelli.jpg")
cv2.imshow("Output", img)
cv2.waitKey(0)

cap = cv2.VideoCapture("../Resources/sorpasso.mp4")
while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

