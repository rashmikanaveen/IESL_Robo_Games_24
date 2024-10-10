import cv2
import numpy as np
import time
import KobukiDriver as kobuki
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SPEED = 120

# Initialize Kobuki
def initialize_kobuki():
    logger.info("Initializing Kobuki robot")
    my_kobuki = kobuki.Kobuki()
    time.sleep(1)  # Allow some time for the robot to initialize
    logger.info("Kobuki robot initialized")
    return my_kobuki

def turn_left(kobuki_bot, ticks):
    logger.debug(f"Turning left for {ticks} ticks")
    kobuki_bot.move(0, SPEED, 0)
    time.sleep(0.1)

def turn_right(kobuki_bot, ticks):
    logger.debug(f"Turning right for {ticks} ticks")
    kobuki_bot.move(SPEED, 0, 0)
    time.sleep(0.1)

def move_forward_optimized(kobuki_bot):
    logger.debug(f"Moving forward with speed {SPEED}")
    kobuki_bot.move(SPEED, SPEED, 0)
    time.sleep(0.1)

def main():
    logger.info("Starting main function")
    # Initialize Kobuki robot
    my_kobuki = initialize_kobuki()

    # Start video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Could not open video stream.")
        return

    logger.info("Starting green object detection. Press 'q' to quit.")
    
    rotation_counter = 0  # To track the number of rotations
    MAX_ROTATIONS = 360    # Assuming each turn_left is ~10 degrees, 3600 degrees total
    push_completed = False
    object_grabed = False  # Initialize the object_grabed variable

    # Create a window for the trackbar
    cv2.namedWindow('Object Detection')

    # Create trackbar for brightness adjustment
    cv2.createTrackbar('Brightness', 'Object Detection', 100, 500, lambda x: None)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to grab frame.")
            break

        # Get the current brightness value from the trackbar
        brightness = cv2.getTrackbarPos('Brightness', 'Object Detection')

        # Apply brightness adjustment
        brightness_factor = brightness / 100.0
        frame = cv2.convertScaleAbs(frame, alpha=brightness_factor, beta=0)
        
        # Update the frame with the adjusted brightness
        processed_frame = frame.copy()

        # Define frame dimensions
        FRAME_WIDTH = frame.shape[1]
        FRAME_HEIGHT = frame.shape[0]
        FRAME_AREA = FRAME_WIDTH * FRAME_HEIGHT

        if not object_grabed:
            # Convert BGR to HSV for green processing
            hsv = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2HSV)

            # Define the lower and upper bounds for green color in HSV
            lower_green1 = np.array([40, 40, 40])
            upper_green1 = np.array([80, 255, 255])

            # Alternatively, for a more precise green detection, you can split into two ranges if needed
            # For simplicity, we'll use a single range here

            # Create mask for green color
            mask = cv2.inRange(hsv, lower_green1, upper_green1)

            # Apply morphological operations to reduce noise
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Find contours for green objects
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            green_object_detected = False
            max_green_area = 0
            largest_green_contour = None

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_green_area:
                    max_green_area = area
                    largest_green_contour = contour

            # Define thresholds
            AREA_THRESHOLD = 500  # Adjust this value based on your requirements

            if largest_green_contour is not None and cv2.contourArea(largest_green_contour) > AREA_THRESHOLD:
                logger.debug("Green object detected")
                green_object_detected = True
                # Compute the center and radius of the contour
                (x, y), radius = cv2.minEnclosingCircle(largest_green_contour)
                center = (int(x), int(y))
                radius = int(radius)

                # Draw the circle
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                
                # Draw a point at the center
                cv2.circle(frame, center, 5, (0, 255, 0), -1)

                cX, cY = center

                # Determine position
                if cX < FRAME_WIDTH * 0.25:
                    position = 'left'
                elif cX > FRAME_WIDTH * 0.75:
                    position = 'right'
                else:
                    position = 'center'

                # Determine distance based on object's vertical position
                bottom_threshold = FRAME_HEIGHT * 0.8  # Consider bottom 20% of the screen as 'near'
                if cY > bottom_threshold:
                    distance = 'near'
                else:
                    distance = 'far'

                logger.debug(f"Object position: {position}, distance: {distance}")

                # Check if object is grabbed
                if distance == 'near':
                    object_grabed = True
                    logger.info("Object grabbed.")
                    continue  # Skip further actions in this frame

                # Decide action based on position and distance
                if position == 'left':
                    turn_left(my_kobuki, 1)
                    cv2.putText(frame, "Turning Left", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif position == 'right':
                    turn_right(my_kobuki, 1)
                    cv2.putText(frame, "Turning Right", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif position == 'center':
                    if distance == 'far':
                        # Move towards the object
                        move_forward_optimized(my_kobuki)
                        cv2.putText(frame, "Moving Forward", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                rotation_counter = 0  # Reset rotation counter when object is detected

            if not green_object_detected:
                # Object not detected
                if rotation_counter >= MAX_ROTATIONS:
                    logger.info("Object not found after maximum rotations. Stopping.")
                    my_kobuki.move(0, 0, 0)
                    cv2.putText(frame, "Object not found. Stopping.", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    break
                else:
                    turn_left(my_kobuki, 10)
                    rotation_counter += 1
                    logger.debug(f"Searching... Rotation {rotation_counter*10}°")
                    cv2.putText(frame, f"Searching... Rotation {rotation_counter*10}°", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        else:
            # Object has been grabbed, proceed to find another green object
            # Draw a black box covering the bottom 20% of the screen
            black_box_start = int(FRAME_HEIGHT * 0.8)
            cv2.rectangle(frame, (0, black_box_start), (FRAME_WIDTH, FRAME_HEIGHT), (0, 0, 0), -1)

            # Convert BGR to HSV for green processing
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define the lower and upper bounds for green color in HSV with reduced sensitivity
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])

            # Create mask for green color
            mask = cv2.inRange(hsv, lower_green, upper_green)

            # Apply morphological operations to reduce noise
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Find contours for green objects
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            target_green_detected = False
            max_green_area = 0
            largest_target_green_contour = None

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_green_area:
                    max_green_area = area
                    largest_target_green_contour = contour

            # Define threshold for stopping
            STOP_AREA_THRESHOLD = FRAME_AREA * 0.15

            if largest_target_green_contour is not None and cv2.contourArea(largest_target_green_contour) > 0:
                target_green_detected = True
                current_green_area = cv2.contourArea(largest_target_green_contour)
                logger.debug(f"Target green area: {current_green_area}")

                # Compute the center of the contour
                M = cv2.moments(largest_target_green_contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    cX, cY = 0, 0

                # Draw the contour and center
                cv2.drawContours(frame, [largest_target_green_contour], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1)

                # Determine position
                if cX < FRAME_WIDTH * 0.3:
                    position = 'left'
                elif cX > FRAME_WIDTH * 0.7:
                    position = 'right'
                else:
                    position = 'center'

                logger.debug(f"Target green position: {position}")

                # Decide action based on position
                if position == 'left':
                    turn_left(my_kobuki, 1)
                    cv2.putText(frame, "Turning Left to Green", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif position == 'right':
                    turn_right(my_kobuki, 1)
                    cv2.putText(frame, "Turning Right to Green", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif position == 'center':
                    # Move towards the green object
                    move_forward_optimized(my_kobuki)
                    cv2.putText(frame, "Moving Forward to Green", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Check if the green area exceeds the threshold
                if current_green_area > STOP_AREA_THRESHOLD:
                    logger.info("Large green object detected. Stopping.")
                    my_kobuki.move(0, 0, 0)
                    cv2.putText(frame, "Green object large. Stopping.", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    push_completed = True
                    break

                rotation_counter = 0  # Reset rotation counter when target is detected

            if not target_green_detected:
                # Green object not detected
                if rotation_counter >= MAX_ROTATIONS:
                    logger.info("Target green object not found after maximum rotations. Stopping.")
                    my_kobuki.move(0, 0, 0)
                    cv2.putText(frame, "Target Green object not found. Stopping.", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    break
                else:
                    turn_left(my_kobuki, 1)
                    rotation_counter += 1
                    logger.debug(f"Searching for Green... Rotation {rotation_counter*10}°")
                    cv2.putText(frame, f"Searching for Green... Rotation {rotation_counter*10}°", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the resulting frame with drawings
        cv2.imshow('Object Detection', frame)

        # Break the loop on 'q' key press or if pushing is completed
        if cv2.waitKey(1) & 0xFF == ord('q') or push_completed:
            logger.info("Exiting main loop")
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()
    # Stop the robot
    my_kobuki.move(0, 0, 0)
    logger.info("Task Completed. Shutting down!")
    # Terminate the code
    logger.info("Terminating the program")
    exit()  # Exit the program

if __name__ == "__main__":
    main()
