import numpy as np
import freenect
import cv2
import time
import KobukiDriver as kobuki

print("Starting camera")
capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
print("Captured camera")

prev_frame_time = 0
new_frame_time = 0
kP = 0.05
kD = 0.1

# def main():
my_kobuki = kobuki.Kobuki()

    # Play start up sound
    # my_kobuki.play_on_sound()

while True:
        frame, timestamp = freenect.sync_get_video()
        new_frame_time = time.time()

        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        fps = 1 / (new_frame_time - prev_frame_time)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        height, width = gray.shape
        gray = gray[height // 2 :, :]  # Crop the lower half of the image

        # Apply Gaussian blur to reduce noise
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply a threshold to create a binary image
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # kernel = np.ones((3,3), np.uint8)
        # thresh = cv2.erode(thresh, kernel, iterations=5)
        # thresh = cv2.dilate(thresh, kernel, iterations=9)

        # Find contours in the binary image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Line-following logic
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            moments = cv2.moments(largest_contour)
            if moments['m00'] != 0:
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

                # Determine whether to turn left or right based on the line position (centered or not)
                if cx < frame.shape[1] // 2:
                    # Turn left
                    my_kobuki.move(100, 255, 0)
                    print("Turn left")
                else:
                    # Turn right
                    my_kobuki.move(255, 100, 0)
                    print("Turn right")

            blackbox = cv2.minAreaRect(contours[0])
            (x_min, y_min), (w_min, h_min), ang = blackbox
            # if ang < -45:
            #      ang = 90 + ang
            # if w_min > h_min and ang > 0:
            #      ang = (90 - ang)*-1
            # if w_min > h_min and ang < 0:
            #      ang = 90 + ang
                    
            setpoint = frame.shape[1] // 2
            error1 = cx - setpoint
            error2 = int(x_min - setpoint)
            ang = int(ang)
            box = cv2.boxPoints(blackbox)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 3)
            cv2.putText(frame, str(int(error1)), (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(frame, str(int(error2)), (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
            cv2.putText(frame, str(int(w_min)), (10, 300), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
            cv2.putText(frame, str(int(h_min)), (10, 340), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(frame, str(int(ang)), (10, 160), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            # cv2.line(frame, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)

            # if error1 < 0:
            #     my_kobuki.move(255, 255-error1, 0)
            # else:
            #     my_kobuki.move(255-error1, 255, 0)

        prev_frame_time = new_frame_time

        cv2.putText(frame, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        # cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)

        # Display the original and masked images
        cv2.imshow("Masked Image", thresh)
        cv2.imshow("Unmasked Image", frame)

        if cv2.waitKey(10) == ord("q"):
            break

capture.release()
cv2.destroyAllWindows()