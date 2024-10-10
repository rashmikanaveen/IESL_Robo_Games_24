# Raspberry Pi Object Tracking Guide

This guide provides steps to set up Raspberry Pi 5 and Raspberry Pi 3 to detect green and red objects, respectively. The devices are used with Kobuki robots for object detection and tracking tasks.

## Raspberry Pi 5: Green Object Detection

### Steps:
1. **Turn On the Kobuki**  
   Ensure the Kobuki robot is powered on before proceeding.

2. **Connect Raspberry Pi 5 to a Screen**  
   Connect the Raspberry Pi 5 to a monitor to check the setup visually.

3. **Press the Button on Raspberry Pi 5**  
   Press the appropriate button on the Pi to begin booting or starting the process.

4. **Ensure the Same Wi-Fi Network**  
   Make sure that both your laptop and Raspberry Pi 5 are connected to the same Wi-Fi network.

5. **Find Raspberry Pi's IP Address**  
   Use the Angry IP Scanner to detect the IP address of the Raspberry Pi.

6. **Connect Using RealVNC Viewer**  
   Use RealVNC Viewer to connect to Raspberry Pi from your laptop via the IP address.

7. **Run the Green Ball Detection Script**  
   Navigate to the relevant folder and run the script to detect the green object:
   
   ```bash
   cd Desktop
   cd New
   cd demo

* To track and place the green ball once, run:
```python
python3 finalgreenball.py
```
* To track and place the green ball in a continuous loop, run:
```python
python3 finalgreenballinfinite.py
```

## Raspberry Pi 3: Red Object Detection

### Steps:
1. **Boot from USB (if applicable)**
If you are using a USB for booting instead of an SD card:
- Remove all USB devices except the bootable USB.
- Connect other USB devices after the booting process is complete.

2. **Turn On the Kobuki**
Ensure the Kobuki robot is powered on.

3. **Connect Raspberry Pi 3 to a Screen**
Similar to the Raspberry Pi 5, it is recommended to connect a monitor for checking the setup.

4. **Ensure the Same Wi-Fi Network**
Ensure both your laptop and Raspberry Pi 3 are connected to the same Wi-Fi network.

5. **Find Raspberry Pi's IP Address**
Use Angry IP Scanner to find the IP address of Raspberry Pi 3.

6. **Connect Using RealVNC Viewer**
Connect to Raspberry Pi 3 using RealVNC Viewer via its IP address.

7. **Run the Red Object Detection Script**
Open the terminal and navigate to the relevant folder to run the red object detection script.

```bash
cd Desktop
source ./bin/activate
cd 'New folder'
cd Kobuki-python
cd demo
```
* To track and place the red object once, run:
```python
python testFinalOnce.py
```
* To track and place the red object in a continuous loop, run:
```python
python testFinalInfinity.py
```
## Troubleshooting
If you encounter any issues, feel free to contact the following people for assistance:

Sahan - 0765820661
Rashmika - 0787057255
Dineth - 0714559195

*** 
Note:
If you modify anything within Raspberry Pi, remember to adjust the paths accordingly. 
***
