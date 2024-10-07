from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

RED = 1
GREEN = 2
BLUE = 3

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="ball video.mp4")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "red"
# ball in the HSV color space, then initialize the
# list of tracked points
redLower = (0, 50, 150)
redUpper = (20, 255, 255)
blueLower = (100, 110, 150)
blueUpper = (120, 255, 255)
pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
    cv2.VideoCapture('ball video.mp4')
# vs =
# vs = VideoStream(src=1).start()
# allow the camera or video file to warm up
print(vs)
time.sleep(2.0)
    
def loop():
    #print("kobuki running..")
    balls = []
    boxes = []

    # grab the current frame
    frame = vs.read()
    
    cv2.imshow("Cap", frame)
    # print(ret, frame)
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        print("No video")

    # resize the frame, blur it, and convert it to the HSV
    # color space

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    print(hsv[0][0])
    # construct a maskRed for the color "red", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the maskRed
    

    maskBlue = cv2.inRange(hsv, blueLower, blueUpper)
    maskBlue = cv2.erode(maskBlue, None, iterations=2)
    maskBlue = cv2.dilate(maskBlue, None, iterations=2)

    maskRed = cv2.inRange(hsv, redLower, redUpper)
    maskRed = cv2.erode(maskRed, None, iterations=2)
    maskRed = cv2.dilate(maskRed, None, iterations=2)

    
    # find contours in the maskRed and initialize the current
    # (x, y) center of the ball
    cntsRed = cv2.findContours(maskRed.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cntsBlue = cv2.findContours(maskBlue.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    
    cntsRed, cntsBlue = imutils.grab_contours(cntsRed), imutils.grab_contours(cntsBlue)


    # only proceed if at least one contour was found
    if len(cntsRed) > 0:
        # find the largest contour in the maskRed, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cv2.drawContours(frame,cntsRed,-1,(100,100,0),2)
        for cnt in cntsRed:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03*peri, True)
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            x, y = int(x), int(y)
            if len(approx)>6:
                shape = "Circle"
                ball = {
                    "center" : (x,y),
                    "radius" : int(radius),
                    "color" : RED
                }
                balls.append(ball)
            else:
                shape = "Square"
                box = {
                    "center" : (x,y),
                    "radius" : int(radius),
                    "color" : RED
                }
                boxes.append(box)
            cv2.putText(frame, shape,(x,y), cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            cv2.drawContours(frame,approx,-1,(0,255,0),5)


    #Blue +++++++++++++++++++
    if len(cntsBlue) > 0:
        # find the largest contour in the maskRed, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cv2.drawContours(frame,cntsBlue,-1,(100,100,0),2)
        for cnt in cntsBlue:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03*peri, True)
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            x, y = int(x), int(y)
            if len(approx)>6:
                shape = "Circle"
                ball = {
                    "center" : (x,y),
                    "radius" : int(radius),
                    "color" : BLUE
                }
                balls.append(ball)
            else:
                shape = "Square"
                box = {
                    "center" : (x,y),
                    "radius" : int(radius),
                    "color" : BLUE
                }
                boxes.append(box)
            cv2.putText(frame, shape,(x,y), cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            cv2.drawContours(frame,approx,-1,(0,255,0),5)
        

    
    # print(balls, boxes)
    for ball in balls:
        out = cv2.circle(frame, ball["center"], ball["radius"], (ball["color"]*80,0,0), 1)


        #c = max(cntsRed, key=cv2.contourArea)
        


    cv2.imshow("Frame", frame)
    cv2.imshow("maskRed", maskRed)
    cv2.imshow("maskBlue", maskBlue)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop