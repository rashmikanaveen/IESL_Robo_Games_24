import KobukiDriver as kobuki
import time


def main():
    my_kobuki = kobuki.Kobuki()

    # Play start up sound
    #   my_kobuki.play_on_sound()
    n=0
    while True:
        key=moves[n]
        if key == "w":
            # Move forward
            my_kobuki.move(200, 200, 0)
            time.sleep(1)
            n+=1
            continue

        elif key == "s":
            # Move backward
            my_kobuki.move(-200, -200, 0)
        elif key == "a":
            # Turn left
            for i in range(30):
                my_kobuki.move(0,200, 0)
                time.sleep(0.1)
            print("1")
            n+=1
            continue
        elif key == "d":
            # Turn right
            for i in range(10):
                my_kobuki.move(200,0, 0)
                time.sleep(0.1)
            n+=1
            continue
        elif key == "x":
            # Stop
            my_kobuki.move(0, 0, 0)

        elif key == "q":
            # Quit
            break
      
        #time.sleep(5)
       # my_kobuki.move(0,0, 0)
        # Print sensor data
        #rint(my_kobuki.encoder_data())


if __name__ == "__main__":
    main()
