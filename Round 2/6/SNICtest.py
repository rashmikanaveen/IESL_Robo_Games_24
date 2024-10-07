import cv2
import time
import freenect
import KobukiDriver as kobuki


prev_frame_time = 0
new_frame_time = 0
my_kobuki = kobuki.Kobuki()

def detect_line(img):
    sum_lines=0
    num_lines=0
    flag=False
    temp=[]
    for y in range(240):   
        flag=False
        for x in range(640):
            if(img[y][x]>0):
                if flag==False: temp.append(x)
                flag=True
            if(img[y][x]==0 and flag==True):
                temp.append(x)
                flag=False
        if(len(temp)==2):
            sum_lines+=((temp[0]+temp[1])/2)
            num_lines+=1
        temp=[]
    
    if(num_lines>=10):
        line_pos=sum_lines/num_lines #average
        diff =640/2-line_pos
        print("diff: "+str(diff))
    else:
        print("No line")
        diff=9999
    return diff



def move_forward():
    my_kobuki.move(20, 20, 0)
def stop():
    my_kobuki.move(0, 0, 0)

while True:
    # Load the image from the Kinect and convert to BGR
    rgb, timestamp = freenect.sync_get_video()
   # rgb=cv2.imread("a.jpg")

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
    cv2.imshow("Masked Image", thresh)
    if(detect_line(thresh)<50.0):
        move_forward()
    else:
        stop()         

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
