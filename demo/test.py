from kobukidriver import Kobuki
import time as t
kobuki_instance=Kobuki()

#for i in range(50):
#t.sleep(0.2)#delay for fetching data
#basic_sensor_data=kobuki_instance.basic_sensor_data()
#print(basic_sensor_data)#prints the basic sensor data from the ro
for i in range(100):
    t.sleep(0.1)
    kobuki_instance.move(100.0, 100.0, 0.0)

#kobuki_instance.move(0,0,0)