import KobukiDriver as kobuki
import time
import keyboard
import line
import numpy as np

baseSpeed = 50
maxSpeed = 100

# left, right, forward = False
junctionFound = False
junctionList = []

P = 1
I = 0
D = 5
prevErr = 0
totalErr = 0

my_kobuki = kobuki.Kobuki()

    
def keyboardControl():
    if keyboard.is_pressed('w'):  
        my_kobuki.move(baseSpeed, baseSpeed, 0)
    elif keyboard.is_pressed('s'):  
        my_kobuki.move(-baseSpeed, -baseSpeed, 0)
    elif keyboard.is_pressed('a'):  
        my_kobuki.move(-baseSpeed, baseSpeed, 0)
    elif keyboard.is_pressed('d'):  
        my_kobuki.move(baseSpeed, -baseSpeed, 0)
    else:
        my_kobuki.move(0, 0, 0)

    # Print sensor data
    print(my_kobuki.encoder_data())


def getLineCorrection(err):
    global totalErr
    global prevErr
    totalErr += err
    
    p = err * P
    i = totalErr * I
    d = (err - prevErr) * D

    prevErr = err

    correction = p + d
    return correction

def applyLinePid(correction):
    leftSpeed = baseSpeed + correction
    rightSpeed = baseSpeed - correction

    if leftSpeed < 0:
        leftSpeed = 0
    if rightSpeed < 0:
        rightSpeed = 0
    if leftSpeed >= maxSpeed:
        leftSpeed = maxSpeed
    if rightSpeed >= maxSpeed:
        rightSpeed = maxSpeed

    my_kobuki.move(leftSpeed, rightSpeed, 0)

def pushForward(distance, getReading = False):
    
    encoderData = my_kobuki.encoder_data()
    currRightEncoder = encoderData['Right_encoder']
    currLeftEncoder = encoderData['Left_encoder']

    while encoderData['Left_encoder'] <= currLeftEncoder + distance | encoderData['Right_encoder'] <= currRightEncoder + distance:
        
        if getReading:
            data = line.readCam()
            foundLeft = data['leftPer'] > 10
            foundRight = data['rightPer'] > 10

            if foundLeft:
                left = True
            if foundRight:
                right = True
    
        my_kobuki.move(baseSpeed, baseSpeed, 1)
        encoderData = my_kobuki.encoder_data

    if getReading:
        data = line.readCam()
        foundForward = data['middlePer'] > 5

        if foundForward:
            forward = True


def turnLeft():
    print(" ")
def turnRight():
    print(" ")

def turnBack():
    print(" ")

def placeCube():
    print(" ")
def grabCube():
    print(" ")

def task(junctionList):
    while True:
        data = line.readCam()

        foundLeft = left = data['leftPer'] > 10
        foundRight = right = data['rightPer'] > 10

        if foundLeft | foundRight:
            pushForward(100, True)#

        pushForward(200)#

        readingCount = np.sum([left, right, forward] == 1)
        junctionFound = readingCount >= 2

        if junctionFound:
            nextMove = junctionList.pop[0]
        elif left:
            nextMove = 'l'
            junctionList.pop[0]
        elif right:
            nextMove = 'r'
            junctionList.pop[0]

        if nextMove == 'l':
            turnLeft()
        elif nextMove == 'r':
            turnRight()

        left = right = forward = junctionFound = False

        if junctionList[0] == 'p':
            placeCube()
            turnBack()
            break
        if junctionList[0] == 'g':
            grabCube()
            turnBack()
            break
        
        error = data['error']
        correction = getLineCorrection(error)
        applyLinePid(correction)


def main():
    while True:
        data = line.readCam()

        error = data['error'] * -1
        correction = getLineCorrection(error)
        applyLinePid(correction)

        # line.readCam()
    print(" ")
    

if __name__ == "__main__":
    main()
