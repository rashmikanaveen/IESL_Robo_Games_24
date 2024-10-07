from controller import Robot,Camera,Display
import cv2
import numpy as np
from consts import *

# 
GR_HMIN = 150
GR_HMAX = 220
GR_SMIN = 65
GR_SMAX = 255
GR_VMIN = 162
GR_VMAX = 255

# 
GB_HMIN = 86
GB_HMAX = 100
GB_SMIN = 123
GB_SMAX = 255
GB_VMIN = 50
GB_VMAX = 255

# 
BR_HMIN = 19
BR_HMAX = 46
BR_SMIN = 9
BR_SMAX = 255
BR_VMIN = 50
BR_VMAX = 255

# 
BB_HMIN = 47
BB_HMAX = 85
BB_SMIN = 30
BB_SMAX = 255
BB_VMIN = 50
BB_VMAX = 255


R_HMIN = 121
R_HMAX = 179
R_SMIN = 13
R_SMAX = 255
R_VMIN = 50
R_VMAX =255


B_HMIN = 101
B_HMAX = 117
B_SMIN = 111
B_SMAX = 255
B_VMIN = 50
B_VMAX = 255


W_HMIN = 0
W_HMAX = 179
W_SMIN = 0
W_SMAX = 92
W_VMIN = 122
W_VMAX = 255

K_HMIN = 0
K_HMAX = 179
K_SMIN = 0
K_SMAX = 71
K_VMIN = 0
K_VMAX = 65

D_HMIN = 0
D_HMAX = 179
D_SMIN = 0
D_SMAX = 20
D_VMIN = 0
D_VMAX = 20

CLR_GR = 0
CLR_GB = 1
CLR_BR = 2
CLR_BB = 3
CLR_R = 4
CLR_B = 5
CLR_W = 6
CLR_K = 7
CLR_D = 8

# Constants for color margins
min_margin = np.array([
    [GR_HMIN, GR_SMIN, GR_VMIN],
    [GB_HMIN, GB_SMIN, GB_VMIN],
    [BR_HMIN, BR_SMIN, BR_VMIN],
    [BB_HMIN, BB_SMIN, BB_VMIN],
    [R_HMIN, R_SMIN, R_VMIN],
    [B_HMIN, B_SMIN, B_VMIN],
    [W_HMIN, W_SMIN, W_VMIN],
    [K_HMIN, K_SMIN, K_VMIN],
    [D_HMIN, D_SMIN, D_VMIN]
], dtype=np.uint8)

max_margin = np.array([
    [GR_HMAX, GR_SMAX, GR_VMAX],
    [GB_HMAX, GB_SMAX, GB_VMAX],
    [BR_HMAX, Y_SMAX, BR_VMAX],
    [BB_HMAX, BB_SMAX, BB_VMAX],
    [R_HMAX, R_SMAX, R_VMAX],
    [B_HMAX, B_SMAX, B_VMAX],
    [W_HMAX, W_SMAX, W_VMAX],
    [K_HMAX, K_SMAX, K_VMAX],
    [D_HMAX, D_SMAX, D_VMAX]
], dtype=np.uint8)

# Initialize robot, camera, and display
robot = None
camera = None
display = None


# Function to get the color mask
def get_mask(color, img):
    print(color)
    lower = min_margin[color]
    upper = max_margin[color]
    mask = cv2.inRange(img, lower, upper)
    return mask

# Function to initialize robot, camera, and display
def init(_robot):
    global robot, camera, display
    robot = _robot
    camera = robot.getDevice("camera")
    camera.enable(TIME_STEP)
    display = robot.getDevice("display")
    robot.step(TIME_STEP)

# Function to get an RGB image
def get_image_rgb():    
    image = camera.getImage()

    if image:
        imageMat = np.frombuffer(image, np.uint8).reshape((IMAGE_HEIGHT, IMAGE_WIDTH, 4))
        imageRGB = cv2.cvtColor(imageMat, cv2.COLOR_BGRA2RGB)
        return imageRGB

    return None

# Function to display an RGB image
def show_image_rgb(image_rgb):    
    image_ref = display.imageNew(image_rgb.tobytes(), display.RGB, IMAGE_WIDTH, IMAGE_HEIGHT)
    display.imagePaste(image_ref, 0, 0, False)
    display.imageDelete(image_ref)

# Function to display a grayscale image
def show_image_grey(image_grey):
    image_rgb = cv2.cvtColor(image_grey, cv2.COLOR_GRAY2RGB)
    show_image_rgb(image_rgb)

# Function to show a preview of the camera feed
def show_preview(color=-1):
    while robot.step(TIME_STEP) != -1:
        image_rgb = get_image_rgb()
        if image_rgb is not None:
            if color > -1:
                image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
                mask = get_mask(color, image_hsv)
                show_image_grey(mask)
            else:
                show_image_rgb(image_rgb)

# Function to save an image
def save_image():    
    i = 6
    filename = "imgs/{}.png".format(i)
    i += 1
    print("Saving {}: {}".format(filename, camera.saveImage(filename, 0)))

# Function to activate image sampling with the spacebar
def activate_sampling():
    keyboard = robot.getKeyboard()
    keyboard.enable(TIME_STEP)
    
    key_prev = -1
    
    while robot.step(TIME_STEP) != -1:
        key_now = keyboard.getKey()
        if key_prev != key_now:
            if key_now == 32:
                save_image()
            key_prev = key_now

# Function to get the contour with the maximum area
def get_max_area_contour_id(contours):
    max_area = 0
    id = 0
    for j, contour in enumerate(contours):
        new_area = cv2.contourArea(contour)
        if new_area > max_area:
            max_area = new_area
            id = j
    return id, int(max_area)
def get_distance(p1, p2):    
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis

# Function to get the nearest contour
def get_nearest_contour_id(contours, priority_left=True):
    x0, y0 = 0, 0
    x1, y1 = 0, 0
    id0, id1 = -1, -1
    distance0, distance1 = 1024, 1024
    center_point = (IMAGE_WIDTH / 2, IMAGE_HEIGHT - 1)

    for j, contour in enumerate(contours):        
        bottom_point = max(contour, key=lambda p: p[0][1])[0]        
        distance_new = get_distance(bottom_point,center_point)

        if distance_new < distance0:
            distance1, x1, y1, id1 = distance0, x0, y0, id0
            distance0, x0, y0, id0 = distance_new, bottom_point[0], bottom_point[1], j
        elif distance_new < distance1:
            distance1, x1, y1, id1 = distance_new, bottom_point[0], bottom_point[1], j

    if priority_left and id1 != -1 and (distance1 - distance0) < 3:
        if x1 < x0:
            return id1, x1, y1
    return id0, x0, y0

# Function to draw points along a contour
def draw_cont_points(image_rgb, contour):
    for point in contour:
        cv2.circle(image_rgb, tuple(point[0]), 0, (0, 255, 0), 2)

# Function to draw a point
def draw_point(image_rgb, x, y, r=255, g=255, b=0):
    cv2.circle(image_rgb, (x, y), 0, (r, g, b), 4)

# Function to draw a vertical line
def draw_line_y(image_rgb, y, r=255, g=0, b=255):
    cv2.line(image_rgb, (0, y), (IMAGE_WIDTH, y), (r, g, b))

# Function to draw a horizontal line
def draw_line_x(image_rgb, x, r=255, g=0, b=255):
    cv2.line(image_rgb, (x, 0), (x, IMAGE_HEIGHT), (r, g, b))


# Example usage:
if __name__ == "__main__":
    # Initialize the robot and camera
    init(None)
    
    # Show a preview of the camera feed
