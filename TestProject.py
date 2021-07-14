import cv2
import time
import PoseModule as pm

#cap = cv2.VideoCapture('PoseVideos/9.mp4')
cap = cv2.VideoCapture(0)
pTime = 0
detector = pm.poseDetector()
while cv2.waitKey(1) < 0:
    success, img = cap.read()
    # img = detector.findPose(img, draw=False)
    img = detector.findPose(img, draw=True)
    # lmList = detector.findPosition(img, draw=False)


    #Para ver los FPS en imagen
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
    cv2.putText(img, str(round(fps, 1))+"FPS", (70, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)