import cv2
import numpy as np
import vision
import move
from consts import *
from controller import Robot

# Define constants for image processing

ballNearMargin = 75
ballReachMargin = 127
ballLeftMargin = 24
ballRightMargin = 104

startReachMargin = 75
floorReachMargin = 127
basketReachMargin = 127

otherBallLeftMargin = 35
otheBallRightMargin = 92
otherBallReachMargin = 122


def init(_robot):
    global robot
    robot = _robot


def goto_ball(color):
    max_speed = MAX_SPEED_VISION

    while robot.step(TIME_STEP) != -1:
        imageRGB = vision.get_image_rgb()
        if imageRGB is not None:
            imageHSV = cv2.cvtColor(imageRGB, cv2.COLOR_RGB2HSV)

            mask = vision.get_mask(color, imageHSV)

            contours, hierarchy = cv2.findContours(
                mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # print(contours[0])

            # return

            if len(contours) == 0:
                move.setLeftMotorSpeed(max_speed)
                move.setRightMotorSpeed(-max_speed)
            else:
                nearest_contour_id, nearest_contour_x, nearest_contour_y = vision.get_nearest_contour_id(contours)
                # nearest_contour_id,area = vision.get_max_area_contour_id(contours)

                # contour=contours[nearest_contour_id]
                # bottom_point = max(contour, key=lambda p: p[0][1])[0]
                # nearest_contour_x, nearest_contour_y=bottom_point

                if (
                    nearest_contour_y < ballReachMargin
                    or ballLeftMargin > nearest_contour_x
                    or nearest_contour_x > ballRightMargin
                ):
                    error = IMAGE_WIDTH / 2 - nearest_contour_x

                    if nearest_contour_y > ballNearMargin:
                        max_speed = MAX_SPEED_VISION / 8

                    move.setLeftMotorSpeed(
                        (-error * Kp_VISION * max_speed) + max_speed)
                    move.setRightMotorSpeed(
                        (error * Kp_VISION * max_speed) + max_speed)

                    color_cont = (0, 255, 0)
                    cv2.drawContours(
                        imageRGB, contours, nearest_contour_id, color_cont, 2, cv2.LINE_8, hierarchy, 0)
                    vision.draw_point(
                        imageRGB, nearest_contour_x, nearest_contour_y)
                    vision.draw_line_y(imageRGB, ballNearMargin)

                    color_margin = (255, 0, 255)
                    cv2.line(imageRGB, (ballLeftMargin, ballReachMargin),
                             (ballLeftMargin, IMAGE_HEIGHT - 1), color_margin)
                    cv2.line(imageRGB, (ballRightMargin, ballReachMargin),
                             (ballRightMargin, IMAGE_HEIGHT - 1), color_margin)
                    cv2.line(imageRGB, (ballLeftMargin, ballReachMargin),
                             (ballRightMargin, ballReachMargin), color_margin)

                    vision.show_image_rgb(imageRGB)
                else:
                    move.setLeftMotorSpeed(0)
                    move.setRightMotorSpeed(0)
                    print("Reached")
                    return
