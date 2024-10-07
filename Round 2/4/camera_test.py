import cv2
from control import Controls
from kobuki_driver_test import main
import numpy as np
import freenect


# Function to get RGB and depth data from the Kinect
# def get_depth_and_rgb():
#     depth, timestamp = freenect.sync_get_depth()
#     rgb, timestamp = freenect.sync_get_video()
#     return depth, rgb



def get_line_center(img, x, y):
    
    line = (img[y[0], x[0]:x[1]]==255).astype(np.uint8)
    idx = np.arange(x[0], x[1], 1)
    
    product = np.multiply(line, idx)
    count = np.count_nonzero(line)
    avg = np.sum(product)//count
    return avg, count

controls = Controls()

controls.newControl("c", 0, 255, 17)

#out = cv2.VideoWriter('sample_01.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))
#cap = cv2.VideoCapture('http://192.168.1.100:8080/video')


while True:
    # depth, rgb = get_depth_and_rgb()

    # Convert depth data to a grayscale image
    # depth = depth.astype("uint8") >> 2  # Right shift to make 10-bit data 8-bit
    # depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)
    # rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    
    # resized = cv2.resize(rgb, (640, 480), interpolation = cv2.INTER_LINEAR )
    # out.write(resized)
    #_, rgb = cap.read()
    rgb, _ = freenect.sync_get_video()
    
    c = controls.getValues()['c']

    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, -int(c))

    x = [230, 410] # [x_start, x_end]
    y = [310,310]  # [y_start, y_end]

    cv2.line(rgb, (x[0], y[0]), (x[1], y[1]), (255, 100, 0), 2)
    cv2.line(rgb, (rgb.shape[1]//2, 0), (rgb.shape[1]//2, rgb.shape[0]), (255,255,0), 1)

    
    avg, count = get_line_center(thresh, x, y)
    cv2.circle(rgb, (avg, y[0]), 3, (0,25,255), 3)
    print(count)

    # Display the RGB and depth streams
    cv2.imshow("RGB", rgb)
    cv2.imshow("Threshold", thresh)
    # cv2.imshow("Depth", depth)

    main()

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(50) & 0xFF == ord("q"):
        break


#out.release()
cv2.destroyAllWindows()
