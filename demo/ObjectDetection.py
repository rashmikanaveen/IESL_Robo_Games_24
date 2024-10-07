import cv2
import numpy as np
import time
import KobukiDriver as kobuki
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Kobuki
def initialize_kobuki():
    logger.info("Initializing Kobuki robot")
    my_kobuki = kobuki.Kobuki()
    time.sleep(1)  # Allow some time for the robot to initialize
    logger.info("Kobuki robot initialized")
    return my_kobuki

def turn_left(kobuki_bot, ticks):
    logger.debug(f"Turning left for {ticks} ticks")
    kobuki_bot.move(0, 200, 0)
    time.sleep(0.1)

def turn_right(kobuki_bot, ticks):
    logger.debug(f"Turning right for {ticks} ticks")
    kobuki_bot.move(200, 0, 0)
    time.sleep(0.1)

def move_forward_optimized(kobuki_bot, speed):
    logger.debug(f"Moving forward with speed {speed}")
    kobuki_bot.move(speed, speed, 0)
    time.sleep(0.1)

def push_forward(kobuki_bot, speed):
    logger.info(f"Pushing forward with speed {speed} for {0.1} seconds")
    kobuki_bot.move(speed, speed, 0)
    time.sleep(0.1)
    kobuki_bot.move(0, 0, 0)
    logger.info("Push completed")

def main():
    logger.info("Starting main function")
    # Initialize Kobuki robot
    my_kobuki = initialize_kobuki()

    # Start video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Could not open video stream.")
        return

    logger.info("Starting red ball detection. Press 'q' to quit.")
    
    rotation_counter = 0  # To track the number of rotations
    MAX_ROTATIONS = 360    # Assuming each turn_left is ~10 degrees, 80 degrees total
    push_completed = False

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to grab frame.")
            break

                # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range for red color in HSV
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Create masks for red color
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        # Combine the masks
        red_mask = mask1 + mask2

        # Optional: Apply morphological operations to reduce noise
        kernel = np.ones((5,5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

        # Find contours for red ball
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        red_ball_detected = False
        max_red_area = 0
        largest_red_contour = None

        for contour in red_contours:
            area = cv2.contourArea(contour)
            if area > max_red_area:
                max_red_area = area
                largest_red_contour = contour

        # Define thresholds
        AREA_THRESHOLD = 500  # Adjust this value based on your requirements
        FRAME_WIDTH = frame.shape[1]
        FRAME_HEIGHT = frame.shape[0]

        if largest_red_contour is not None and cv2.contourArea(largest_red_contour) > AREA_THRESHOLD:
            logger.debug("Red ball detected")
            red_ball_detected = True
            # Compute the center of the contour
            M = cv2.moments(largest_red_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            # Draw a circle at the center
            cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
            
            # Draw the contour shape of the ball
            cv2.drawContours(frame, [largest_red_contour], -1, (0, 255, 0), 2)

            # Determine position
            if cX < FRAME_WIDTH * 0.3:
                position = 'left'
            elif cX > FRAME_WIDTH * 0.7:
                position = 'right'
            else:
                position = 'center'

            # Determine distance based on area
            near_area_threshold = (FRAME_HEIGHT / 3) * (FRAME_WIDTH / 3)
            if max_red_area > near_area_threshold:
                distance = 'near'
            else:
                distance = 'far'

            logger.debug(f"Ball position: {position}, distance: {distance}")

            # Decide action based on position and distance
            if position == 'left':
                turn_left(my_kobuki, 1)
                cv2.putText(frame, "Turning Left", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif position == 'right':
                turn_right(my_kobuki, 1)
                cv2.putText(frame, "Turning Right", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif position == 'center':
                if distance == 'far':
                    # Move towards the ball
                    move_forward_optimized(my_kobuki, 100)
                    cv2.putText(frame, "Moving Forward", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif distance == 'near' and not push_completed:
                    logger.info("Ball reached. Pushing forward.")
                    cv2.putText(frame, "Ball Reached. Pushing Forward.", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    push_forward(my_kobuki, speed=100)
                    push_completed = True

            rotation_counter = 0  # Reset rotation counter when ball is detected

        if not red_ball_detected:
            # Object not detected
            if rotation_counter >= MAX_ROTATIONS:
                logger.info("Object not found after maximum rotations. Stopping.")
                my_kobuki.move(0, 0, 0)
                cv2.putText(frame, "Object not found. Stopping.", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                break
            else:
                turn_left(my_kobuki, 10)
                rotation_counter += 1
                logger.debug(f"Searching... Rotation {rotation_counter*10}°")
                cv2.putText(frame, f"Searching... Rotation {rotation_counter*10}°", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

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