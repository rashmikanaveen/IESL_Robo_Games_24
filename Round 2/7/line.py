import cv2
import numpy as np
import freenect
import time

dict = {}

def readCam():
    
    rgb, timestamp = freenect.sync_get_video()
    # rgb = cv2.imread('dog.png')

    img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)  # Convert RGB image to BGR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert BGR to grayscale

    height, width = gray.shape
    gray = gray[height // 2 :, :] 
    rgb = rgb[height // 2 :, :]

    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    lineContours, _ = cv2.findContours(thresh[35: , :], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    allContours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(rgb, allContours, -1, (255, 0, 0), 1)

    shift_x =  0 
    shift_y = 35
    for contour in lineContours:
        shifted_contour = contour.copy()
        shifted_contour[:, 0, 0] += shift_x
        shifted_contour[:, 0, 1] += shift_y
        cv2.drawContours(rgb, [shifted_contour], -1, (255, 0 ,255), 1)

    leftRectPos = (0, 0)
    rightRectPos = (460, 0)
    middleRectPos = (170, 0)
    rectWidth = 169
    rectHeight = 35

    cv2.rectangle(rgb, leftRectPos, (leftRectPos[0] + rectWidth ,leftRectPos[1] + rectHeight), (0,255,0), 1)
    cv2.rectangle(rgb, middleRectPos, (middleRectPos[0] + 289 ,middleRectPos[1] + rectHeight), (0,255,0), 1)
    cv2.rectangle(rgb, rightRectPos, (rightRectPos[0] + rectWidth ,rightRectPos[1] + rectHeight), (0,255,0), 1)
    cv2.rectangle(rgb, (0,35), (629, 239), (0,255,0), 1)

    dict['error'] = None
    if len(lineContours) > 0:
        x, y, w, h = cv2.boundingRect(lineContours[0])
        cv2.rectangle(rgb, (x,y + 35), (x+w , y+h), (0, 0, 255), 1)
        cv2.line(rgb, (x+(w//2), 220), (x+(w//2), 230), (255,0,0), 2)
        # cv2.arrowedLine(rgb, (x+(w//2), 210), (x+(w//2), 230), (255,0,0), thickness=2, tipLength=0.4)
        # print(f"{x} {y} {w} {h}")
        dict['error'] = (x + (w // 2)) - (width // 2)

    left = thresh[:rectHeight, :rectWidth]
    right = thresh[:rectHeight, rightRectPos[0]:]
    middle = thresh[:rectHeight, middleRectPos[0]:middleRectPos[0] + 289]

    leftCount = 0
    rightCount = 0
    middleCount = 0
    for line in left:
        leftCount += np.sum(line == 255)
    dict['leftPer'] = ((leftCount) / (rectHeight * rectWidth)) * 100

    for line in right:
        rightCount += np.sum(line == 255)
    dict['rightPer'] = ((rightCount) / (rectHeight * rectWidth)) * 100

    for line in middle:
        middleCount += np.sum(line == 255)
    dict['middlePer'] = ((middleCount) / (rectHeight * 289)) * 100
    
    cv2.imshow("processed_image", thresh)
    cv2.imshow("image", rgb)
    cv2.imwrite('image.png', rgb)

    return dict
