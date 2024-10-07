import cv2
import freenect
import time



# Function to get RGB and depth data from the Kinect
def get_depth_and_rgb():
    depth, timestamp = freenect.sync_get_depth()
    rgb, timestamp = freenect.sync_get_video()
    return depth, rgb


while True:
    depth, rgb = get_depth_and_rgb()

    # Convert depth data to a grayscale image
    depth = depth.astype("uint8") >> 2  # Right shift to make 10-bit data 8-bit
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    # Display the RGB and depth streams
    cv2.imshow("RGB", rgb)
    cv2.imshow("Depth", depth)

    # Exit the loop if the 'q' key is pressed
    key=cv2.waitKey(1)
    if  key== ord("q"):
        break
    elif key==ord("c"):
        cv2.imwrite('./rgb_{}.png'.format(int(time.time())),rgb)
        cv2.imwrite('./depth_{}.png'.format(int(time.time())),depth)
        print("Captured")




cv2.destroyAllWindows()
