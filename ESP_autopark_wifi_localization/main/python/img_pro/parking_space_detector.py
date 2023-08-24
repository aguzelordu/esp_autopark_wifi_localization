import cv2
import pickle
import numpy as np


def checkParkSpace(image):
    spaceCounter = 0
    s = 0

    for pos in posList:
        s += 1
        x, y = pos
        img_crop = image[y: y + height1, x:x + width1]
        slot = cv2.countNonZero(img_crop)

        print(f"slot{s}:", slot)

        if slot < 180:
            color = (0, 255, 0)
            spaceCounter += 1
            full_slot.append(f"s{s}")
        else:
            empty_slot.append(f"s{s}")
            color = (0, 0, 255)
        cv2.rectangle(img, pos, (pos[0] + width1, pos[1] + height1), color, 2)
        #cv2.putText(img,)

def checkNodes(image):
    n = 0

    for pos2 in posList2:
        n += 1
        x, y = pos2
        img_crop = image[y: y + height2, x:x + width2]
        node = cv2.countNonZero(img_crop)

        print(f"node{n}:", node)

        if node < 40:
            color = (255, 128, 0)
            full_node.append(f"n{n}")
        else:
            color = (0, 96, 255)
            empty_node.append(f"n{n}")
        cv2.rectangle(img, pos2, (pos2[0] + width2, pos2[1] + height2), color, 1)


width1 = 22
height1 = 22
width2 = 12
height2 = 12


cap = cv2.VideoCapture("...s1.mp4")  # or scenario2.mp4    # Also can real-time cam record.


with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)
    posList2 = pickle.load(f)


while True:
    success, img = cap.read()
    #cap = cv2.imread("...s1.mp4")

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    imgDilate = cv2.dilate(imgMedian, np.ones((3, 3), np.uint8), iterations=1)

    empty_slot = []
    full_slot = []
    empty_node = []
    full_node = []

    checkParkSpace(imgDilate)
    checkNodes(imgDilate)
    print(empty_slot)
    print(full_slot)
    print()
    print(empty_node)
    print(full_node)
    #blocks that sends slots and nodes

    # cv2.imshow("img-gray", imgGray)
    # cv2.imshow("img-blur", imgBlur)
    # cv2.imshow("img-thresh", imgThreshold)
    # cv2.imshow("img-median", imgMedian)
    cv2.imshow("img-dilate", imgDilate)
    cv2.imshow("img", img)
    cv2.waitKey(10)

