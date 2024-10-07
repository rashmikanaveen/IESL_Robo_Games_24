
from controller import Robot, Motor

def init(_robot):
    global leftMotor,rightMotor,robot
    robot=_robot
    leftMotor = robot.getDevice('left_motor')
    rightMotor = robot.getDevice('right_motor')
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)

def setLeftMotorSpeed(speed):
    leftMotor.setVelocity(speed)

def setRightMotorSpeed(speed):
    rightMotor.setVelocity(speed)
