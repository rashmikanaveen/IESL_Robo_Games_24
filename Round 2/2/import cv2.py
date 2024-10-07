import cv2
import freenect
import numpy as np

# Function to get RGB frame from Kinect sensor
def get_video():
    return freenect.sync_get_video()[0]

# Function to get depth frame from Kinect sensor
def get_depth():
    return freenect.sync_get_depth()[0]

while True:
    # Get RGB and depth frames from Kinect sensor
    video_frame = get_video()
    depth_frame = get_depth()

    # Convert RGB frame to OpenCV format
    video_frame_cv2 = cv2.cvtColor(video_frame, cv2.COLOR_RGB2BGR)

    # Detect objects (green objects in this example)
    lower_green = np.array([100,100,100])])
    upper_green = np.array([85, 255, 255]
    mask = cv2.inRange(video_frame_cv2, lower_green, upper_green)
    green_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through detected objects and calculate distances and angles
    for contour in green_contours:
        area = cv2.contourArea(contour)
        if area > 100:)
            # Calculate object distance using depth information
            x, y, w, h = cv2.boundingRect(contour)
            object_depth = np.mean(depth_frame[y:y+h, x:x+w])  # Mean depth value of the object region
            
            # Calculate angle between camera and object (assuming the camera's field of view)
            focal_length = 525  # Focal length of Kinect 360 camera (in pixels)
            sensor_height = 480  # Height of the Kinect sensor (in pixels)
            object_center_x = x + w // 2
            horizontal_angle = np.arctan((object_center_x - 320) / focal_length) * (180 / np.pi)
            
            print(f"Object at ({object_center_x}, {y + h // 2}) is approximately {object_depth} units away.")
            print(f"Horizontal angle between camera and object: {horizontal_angle} degrees.")

    # Display the masked frame with detected objects
    cv2.imshow("Objects Detection", mask)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release OpenCV windows
cv2.destroyAllWindows()