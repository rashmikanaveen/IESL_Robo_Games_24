import KobukiDriver as kobuki
import time
from pynput import keyboard

from collections import deque
from imutils.video import VideoStream
import numpy as npe
import argparse
import cv2
import imutils
import freenect

kobuki_enabled = True


RED = 1
GREEN = 2
BLUE = 3

# define the lower and upper boundaries of the "red"
# ball in the HSV color space, then initialize the
# list of tracked points
redLower = (0, 50, 150)
redUpper = (20, 255, 255)
blueLower = (100, 110, 100)
blueUpper = (140, 255, 255)
# if a video path was not supplied, grab the reference
# to the webcam


vs = VideoStream(src=0).start()

##########################################################


def main():
    print("Starting up...")
    my_kobuki = kobuki.Kobuki()

    def kill_cam():
        # close all windows
        #cv2.destroyAllWindows()
        pass
    
    def init_cam():
        #vs = VideoStream(src=0).start()
        pass

    def on_press(key):
        try:
            key = key.char
        except:
            return
        print(key)
        if key == 'w':
                my_kobuki.move(200, 200, 0)
        elif key == "e":
            global kobuki_enabled
            kobuki_enabled = not kobuki_enabled
            if not kobuki_enabled:
                my_kobuki.move(0,0,0)
                my_kobuki.play_off_sound()
            else:
                my_kobuki.play_on_sound()
                time.sleep(1)
                init_cam()
            print("kobuki enabled: ", kobuki_enabled)
        elif key == "s":
            my_kobuki.move(-200, -200, 0)
        elif key == "a":
            # Turn left
            my_kobuki.move(-600, 200, 1)
        elif key == "d":
            # Turn right
            my_kobuki.move(200, -600, 1)
        elif key == "x":
            # Stop
            my_kobuki.move(0, 0, 0)
        elif key == "i":
            # info
            print(my_kobuki.basic_sensor_data())
        elif key == "1":
            # Play sound
            my_kobuki.play_button_sound()
        elif key == "2":
            #print("led")
            # LED Control
            my_kobuki.set_led1_green_colour()
            time.sleep(1)
            my_kobuki.set_led2_red_colour()
            time.sleep(1)
            my_kobuki.clr_led1()
            my_kobuki.clr_led2()
        elif key == "q":
            # Quit
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    #listener.join()  # remove if main thread is polling self.keys
    print("Kobuki started successfully...")

    # Play start up sound
    #   my_kobuki.play_on_sound()

    while True:
        if kobuki_enabled:
            balls = []
            boxes = []

            # grab the current frame
            rgb, timestamp = freenect.sync_get_video()
            #print(rgb)
            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            #frame = vs.read()
            if frame is None:
                print("No video")
                break
            cv2.imshow("Cap", frame)
            # if we are viewing a video and we did not grab a frame,
            # then we have reached the end of the video

            # resize the frame, blur it, and convert it to the HSV
            # color space

            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (7, 7), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            #print(hsv[0][0])
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
            if key == ord("q"):
                break


    


        # Print sensor data
        #print(my_kobuki.basic_sensor_data())
        # if not kobuki_enabled:
        #     kill_cam()

if __name__ == "__main__":
    main()
