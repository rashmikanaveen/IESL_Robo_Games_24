import cv2
import freenect
import time

# Function to get RGB and depth data from the Kinect
def get_depth_and_rgb():
    depth, timestamp = freenect.sync_get_depth()
    rgb, timestamp = freenect.sync_get_video()
    return depth, rgb

def save(name,frame_array):
    shape=frame_array[0].shape
    out = cv2.VideoWriter('./{}_{}.mp4'.format(name,int(time.time())),cv2.VideoWriter_fourcc(*'h264'), 30, (shape[1], shape[0]))
    for i in range(len(frame_array)):
        cv2.imshow('Save', frame_array[i])
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
        out.write(frame_array[i])
    out.release()


def main():
    rgb_frame_array = []
    depth_frame_array = []
    
    while True:
        depth, rgb = get_depth_and_rgb()

        # Convert depth data to a grayscale image
        depth = depth.astype("uint8") >> 2  # Right shift to make 10-bit data 8-bit
        depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        # Display the RGB and depth streams
        cv2.imshow("RGB", rgb)
        cv2.imshow("Depth", depth)

        rgb_frame_array.append(rgb)
        depth_frame_array.append(depth)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(10) & 0xFF == ord("q"):
            save('rgb',rgb_frame_array)
            save('depth',depth_frame_array)
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
