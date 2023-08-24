import cv2
import pickle
import numpy as np

width2 = 12
height2 = 12
width1 = 22
height1 = 22

try:
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)  # slot list
        posList2 = pickle.load(f)  #node list
except:
    posList = []
    posList2 = []

def mouseClick(events, x, y, flags, params):      # Coordinates of the left clicked point in the image
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))

    if events == cv2.EVENT_MBUTTONDOWN:
        posList2.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:

        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1+width1 and y1 < y < y1+height1:  # Closes when right-clicking on a point in the drawn box
                posList.pop(i)
        for j, pos2 in enumerate(posList2):
            x2, y2 = pos2
            if x2 < x < x2+width2 and y2 < y < y2+height2:  # Closes when right-clicking on a point in the drawn box
                posList2.pop(j)

    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)     # To save a fileselected fields
        pickle.dump(posList2, f)

for x, y in posList:
    print("slot", x, y)

for x, y in posList2:
    print("node", x, y)

while True:
    img = cv2.imread("...scenario1.jpg")  # or scenario2.jpg    # Also can real-time cam record.


    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width1, pos[1] + height1), (0,255,255), 1)  # Opens a rectangle where clicked
    for pos2 in posList2:
        cv2.rectangle(img, pos2, (pos2[0] + width2, pos2[1] + height2), (255,255,0), 1)

    #print("poslist: ", posList)

    cv2.imshow("img", img)
    cv2.setMouseCallback("img", mouseClick)
    cv2.waitKey(1)


