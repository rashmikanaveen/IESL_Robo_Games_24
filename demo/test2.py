import cv2
import freenect
import time
import KobukiDriver as kobuki

prev_frame_time = 0
new_frame_time = 0

while True:
    my_kobuki = kobuki.Kobuki()
    # Load the image from the Kinect and convert to BGR
    rgb, timestamp = freenect.sync_get_video()

    new_frame_time = time.time()
    # Calculate frames per second (fps)
    fps = 1 / (new_frame_time - prev_frame_time)

    img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)  # Convert RGB image to BGR

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert BGR to grayscale
    height, width = gray.shape
    gray = gray[height // 2 :, :]  # Crop the lower half of the image

    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    prev_frame_time = new_frame_time

    # Display the frames per second (fps) on the image
    cv2.putText(img, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
    cv2.imshow("Depth",thresh)
    # Display the original and masked images
    if fps > 0:

 

        if fps >= 120:

            print("Turn Left!")
            my_kobuki.move(200, 200, 0)
 

        if fps < 120 and fps > 50:

            my_kobuki.move(-100, 100, 0)

 

        if fps <= 50:

            my_kobuki.move(100, -100, 0)

 

    else:

        print ("I don't see the line")

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
