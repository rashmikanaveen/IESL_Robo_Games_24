import KobukiDriver as kobuki
import time

T_KP = 0
T_KD = 0

MIDSPEED = 300
MAXSPPED = 500
MINSPEED = 100

my_kobuki = kobuki.Kobuki()

def turn_with_encoder(count,dir):
    print(my_kobuki.encoder_data()["Left_encoder"])
    initial_l_value = int(my_kobuki.encoder_data()["Left_encoder"])
    initial_r_value = int(my_kobuki.encoder_data()["Right_encoder"])

    if dir == 'l':
        while (my_kobuki.encoder_data()["Right_encoder"]<count+initial_r_value):
            my_kobuki.move(0, MIDSPEED, 0) 
            print(my_kobuki.encoder_data())
    else:
        while (my_kobuki.encoder_data()["Left_encoder"]<count+initial_l_value):
            my_kobuki.move(MIDSPEED, 0, 0)
            print(my_kobuki.encoder_data()) 

    my_kobuki.move(0, 0, 0) 
    

def main():


    # Play start up sound
    my_kobuki.play_on_sound()
    # key = input("Enter command: ")
    
        # Move forwardw
    my_kobuki.move(MIDSPEED,MIDSPEED, 0) 
    my_kobuki.move(0,0, 0)      
    # while(True):
    while True:
       
        # key = input("Enter command: ")
        # if key == "w":
        #     # Move forwardw
        #     my_kobuki.move(MIDSPEED, MIDSPEED, 0)
        # elif key == "s":
        #     # Move backward
        #     my_kobuki.move(-MIDSPEED, -MIDSPEED, 0)
        # elif key == "a":
        #     # Turn left
        #     my_kobuki.move(MIDSPEED, MIDSPEED, 1) 
        # elif key == "d":
        #     # Turn right
        #     my_kobuki.move(-MIDSPEED, MIDSPEED, 1)
        # elif key == "x":
        #     # Stop
        #     my_kobuki.move(0, 0, 0)
        # elif key == "1":
        #     # Play sound
        #     my_kobuki.play_button_sound()
        # elif key == "2":
        #     # LED Control
        #     my_kobuki.set_led1_green_colour()
        #     time.sleep(1)
        #     my_kobuki.set_led2_red_colour()
        #     time.sleep(1)
        #     my_kobuki.clr_led1()
        #     my_kobuki.clr_led2()
        # elif key == "q":
        #     # Quit
        #     break

        # # Print sensor data
       
        key = input("Enter command: ")
  
 
        if key == "a":
        # Move forwardw
            turn_with_encoder(4500,'l')        
    
        if key == "d":
        # Move forwardw
            turn_with_encoder(4500,'r')  
        # print(my_kobuki.winertial_sensor_data())
        # while(True):w
        #     print(my_kobuki.gyro_velocity_data())

       
    

    # while True:
    #     key = input("Enter command: ")
    #     if key == "w":
    #         # Move forward
    #         my_kobuki.move(200, 200, 0)
    #     elif key == "s":
    #         # Move backward
    #         my_kobuki.move(-200, -200, 0)
    #     elif key == "a":
    #         # Turn left
    #         my_kobuki.move(100, -100, 0) 
    #     elif key == "d":
    #         # Turn right
    #         my_kobuki.move(-100, 100, 0)
    #     elif key == "x":
    #         # Stop
    #         my_kobuki.move(0, 0, 0)
    #     elif key == "1":
    #         # Play sound
    #         my_kobuki.play_button_sound()
    #     elif key == "2":
    #         # LED Control
    #         my_kobuki.set_led1_green_colour()
    #         time.sleep(1)
    #         my_kobuki.set_led2_red_colour()
    #         time.sleep(1)
    #         my_kobuki.clr_led1()
    #         my_kobuki.clr_led2()
    #     elif key == "q":
    #         # Quit
    #         break

    #     # Print sensor data
    #     print(my_kobuki.encoder_data())



if __name__ == "__main__":

    main()


def turn_angle(theta,dir):
    initial_theta = my_kobuki.inertial_sensor_data()["angle"]
    if dir == "l":
        final_theta = initial_theta + theta
    else:
        final_theta = initial_theta - theta    

    t_kp = T_KP
    t_kd = T_KD
    prev_error = 0

    while(True):
        error = final_theta - my_kobuki.inertial_sensor_data()["angle"]
        if abs(error)<2:
            break
        vel = error*t_kp + (error - prev_error)*t_kd

        if abs(vel)>255:
            vel = 255*vel/abs(vel)

        my_kobuki.move(vel, -1*vel, 0) 
        prev_error = error 
          
    my_kobuki.move(0, 0, 0)

def curve_path(heading_angle, dir):
    while abs(heading_angle - my_kobuki.inertial_sensor_data()["angle"])>3:
        if dir == "l":
            my_kobuki.move(150, 100, 0) 
        else:
            my_kobuki.move(100, 150, 0)    

    my_kobuki.move(0, 0, 0)

def turn_angle(theta,dir):
    initial_theta = my_kobuki.inertial_sensor_data()["angle"]
    if dir == "l":
        final_theta = initial_theta + theta
    else:
        final_theta = initial_theta - theta    

    t_kp = T_KP
    t_kd = T_KD
    prev_error = 0

    while(True):
        error = final_theta - my_kobuki.inertial_sensor_data()["angle"]
        if abs(error)<2:
            break
        vel = error*t_kp + (error - prev_error)*t_kd

        if abs(vel)>255:
            vel = 255*vel/abs(vel)

        my_kobuki.move(vel, -1*vel, 0) 
        prev_error = error 
          
    my_kobuki.move(0, 0, 0)

def go_straight():
    pass

