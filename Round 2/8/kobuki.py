import KobukiDriver as kobuki
import time




def main():
    my_kobuki = kobuki.Kobuki()

    my_kobuki.play_button_sound()

    # Play start up sound
    #   my_kobuki.play_on_sound()

    while True:
        key = input("Enter command: ")
        if key == "w":
            # Move forward
            my_kobuki.move(200, 200, 0)
        elif key == "s":
            # Move backward
            my_kobuki.move(-200, -200, 0)
        elif key == "a":
            # Turn left
            my_kobuki.move(100, -100, 0)
        elif key == "d":
            # Turn right
            my_kobuki.move(-100, 100, 0)
        elif key == "x":
            # Stop
            my_kobuki.move(0, 0, 0)
        elif key == "1":
            # Play sound
            my_kobuki.play_button_sound()
        elif key == "2":
            # LED Control
            my_kobuki.set_led1_green_colour()
            time.sleep(1)
            my_kobuki.set_led2_red_colour()
            time.sleep(1)
            my_kobuki.clr_led1()
            my_kobuki.clr_led2()
        elif key == "q":
            # Quit
            break

        # Print sensor data
        print(my_kobuki.encoder_data())

        print(my_kobuki.encoder_data())
        left = my_kobuki.encoder_data()["Left_encoder"]
        rev = left*52

        def moveRevs(revs):

            leftStart = my_kobuki.encoder_data()["Left_encoder"]
            startRev = leftStart*52
            
            while(True):
                endLeft = my_kobuki.encoder_data()["Left_encoder"]

                endRev = endLeft*52
                
                diffRev = endRev - startRev
                print("moving forward", endRev, diffRev)

                if (diffRev >= revs):
                    break    
                my_kobuki.move(100, 100, 0)
                time.sleep(1)

            my_kobuki.move(0,0,0)
        moveRevs(29068*30)
        
        counter = 0
        while(counter < 100):
            counter += 1
            my_kobuki.move(100, -100, 0)


if __name__ == "__main__":
    main()
