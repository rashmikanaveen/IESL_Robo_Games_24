import time
import KobukiDriver as kobuki
import cv2
import math

turns = []
isLineDetected = False
hasLineDisappeared = False
turnNo = 0

diastanceToStop = (4.6 + 19)*10
wheelCur = 0 + 2*35*math.pi
speedReductor = 1
speed = 255



robot = kobuki.Kobuki()
robot.play_button_sound()
print(robot.encoder_data())
left = robot.encoder_data().left
rev = left*52


def moveRevs(revs):

    left = robot.encoder_data().left
    startRev = left*52
    
    while(True):
        
        left = robot.encoder_data().left
        endRev = left*52
        
        diffRev = endRev - startRev
        if (revs >= diffRev):
            break    
        kobuki.move(100, 100)



def gerErrorAndSpeed(prcsd_img, enc_val):
    global speed
    global isLineDetected
    global speedReductor
    global hasLineDisappeared
    global turnNo

    line_bend_threshold = 100
    white_Xs = []

    img = cv2.imread(prcsd_img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w, _ = img.shape

    for row in range (h, 0, -1):
        for column in range (w):
            if img[row, column] == 255:
                white_Xs.append(column)

    whiteWidth = max(white_Xs) - min(white_Xs)

    lineMidPixel = (max(white_Xs) + min(white_Xs))/2
    center = w/2
    error = center - lineMidPixel

    if whiteWidth < line_bend_threshold:
        if isLineDetected:
            speed -= speedReductor

            initial_enc_val = enc_val
            hasLineDisappeared = True
            isLineDetected = False
        elif hasLineDisappeared:
            speed -= speedReductor

            if enc_val - initial_enc_val >= diastanceToStop:
                turns[turnNo]()

                hasLineDisappeared = False
                turnNo += 1
                speed = 255


    else:
        isLineDetected = True
        speed -= speedReductor

    return error, speed






moveRevs(20)