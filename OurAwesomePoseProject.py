# https://youtu.be/brwgBf6VB0I
# JOINTS: https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png

import getopt
import sys
import time

import cv2

import PoseModule as pm


def main(argv):
    #Regocemos los argumentos
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print
        'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)



    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = pm.poseDetector()
    while cv2.waitKey(1) < 0:
        success, img = cap.read()
        img = detector.findPose(img, draw=True)
        lmList = detector.findPosition(img, draw=True)
        # if len(lmList) != 0:
            # print(lmList[14]) #Posicion del joint 14
            # print("\n\n\n")
            # print(*lmList) #Posicion de todos los joints
            # print(*lmList, sep="\n")
            # cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
            #detector.findAngle(img,11,13,15,draw=True) #angulo del codo con el hombro y la muñeca
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(img, str(round(fps, 1)) + "FPS", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    print(" ESTAMOS EN OurAwesomePoseProject.py")
    main(sys.argv[1:])