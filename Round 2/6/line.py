import cv2
import time

prev_frame_time = 0
new_frame_time = 0
my_kobuki = kobuki.Kobuki()


def detect_line(input_img):
    # Canny Edge Detection
    img_edges = cv2.Canny(image=input_img, threshold1=100, threshold2=200)
    # Display Canny Edge Detection Image
    cv2.imshow('Canny Edge Detection', img_edges)
    lines=[]
    temp=[]
    for y in range(240):   
        for x in range(640):
            if(img_edges[y][x]>0):
                temp.append(x)
        if(len(temp)==2):
            lines.append((temp[0]+temp[1])/2)
        temp=[]
    
    if(len(lines)>=10):
        #line_pos=sum(lines)/len(lines) #average
        #diff =640/2-line_pos
        #print("diff: "+str(diff))
        return True
    else:
        print("No line")
        return False

def move_forward():
    my_kobuki.move(200, 200, 0)

while True:
    # Load the image from the Kinect and convert to BGR
    rgb, timestamp = freenect.sync_get_video()
    #rgb=cv2.imread("sc2.png")

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

    # Display the original and masked images
    cv2.imshow("Unmasked Image", rgb)
    #cv2.imshow("Masked Image", thresh)

    if(detect_line(gray)):
        move_forward()         

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
