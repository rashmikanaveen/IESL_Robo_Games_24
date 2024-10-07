import KobukiDriver as kobuki
import time

my_kobuki = kobuki.Kobuki()
class Kobuki(kobuki.Kobuki):
    def move_forward(self, distance, speed):
        # Calculate the time to move
        time_to_move = distance / speed

        # Start moving
        self.move(speed, speed, 0)

        # Wait for the specified time
        time.sleep(time_to_move)

        # Stop moving
        self.move(0, 0, 0)

    
    def move_backword(self, distance, speed):
        # Calculate the time to move
        time_to_move = distance / speed

        # Start moving
        self.move(-speed, -speed, 0)

        # Wait for the specified time
        time.sleep(time_to_move)

        # Stop moving
        self.move(0, 0, 0)
    
    def turn(self, angle, speed):
        # Calculate the time to turn
        # This will depend on the specifics of your robot
        time_to_turn = angle / speed

        # Start turning
        # To turn right
        self.move(speed, -speed, 0)

        # Wait for the specified time
        time.sleep(time_to_turn)

        # Stop moving
        self.move(0, 0, 0)

    def turnback(self, angle, speed):
        # Calculate the time to turn
        # This will depend on the specifics of your robot
        time_to_turn = angle / speed

        # Start turning
        # To turn right
        self.move(-speed, speed, 0)

        # Wait for the specified time
        time.sleep(time_to_turn)

        # Stop moving
        self.move(0, 0, 0)

#lets consider
distance = 25
angle = 30
speed=5 # take usual speed


    
my_kobuki.turn(angle,speed)
my_kobuki.move_forward(distance,speed)
my_kobuki.turnback(angle,speed)