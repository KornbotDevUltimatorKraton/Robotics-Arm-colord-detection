#python color_tracking.py --video balls.mp4
#python color_tracking.py

# import the necessary packages
#from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import pyfirmata
import math  
import time 
#import urllib #for reading image from URL


# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video",
 #   help="path to the (optional) video file")
#ap.add_argument("-b", "--buffer", type=int, default=64,
 #   help="max buffer size")
#args = vars(ap.parse_args())
 
# define the lower and upper boundaries of the colors in the HSV color space
lower = {'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255)}

# define standard colors for circle around the object
colors = {'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217)}
AngleCam = 0 
#pts = deque(maxlen=args["buffer"])
hardware = pyfirmata.ArduinoMega("/dev/ttyACM0") # hardware connection 
base = hardware.get_pin('d:5:s')
shoulder = hardware.get_pin('d:6:s')
elbow = hardware.get_pin('d:7:s')
wrist = hardware.get_pin('d:4:s')
wristrotate = hardware.get_pin('d:8:s')
gripper = hardware.get_pin('d:9:s')

# if a video path was not supplied, grab the reference
# to the webcam
#cv2.namedWindow("Window")
camera = cv2.VideoCapture(0)
# otherwise, grab a reference to the video file
# keep looping
def Cameraviewbase(x,y):
     xbase = (x/640)*180
     ybase = (y/480)*180
     Thetabase = math.atan(ybase/xbase)
     return Thetabase 
def Settingfreeze(sholAngle,elboAngle,wristAngle,WristrotAngle,GripperAngle):
     shoulder.write(sholAngle)
     elbow.write(elboAngle)
     wrist.write(wristAngle)
     wristrotate.write(WristrotAngle)
    # gripper.write(GripperAngle)
def GripperWorks(key,sholAngle,elboAngle,wristAngle,WristrotAngle,GripperAngle):
     if key == 'yellow': 
           for i in range(120,sholAngle):
              shoulder.write(sholAngle)
              elbow.write(elboAngle)
              wrist.write(wristAngle)
              wristrotate.write(WristrotAngle)
              #time.sleep(0.01)
              if i == sholAngle:
                  gripper.write(GripperAngle)
  #   elif key == 'blue': 
   #           shoulder.write(sholAngle-10)
    #          elbow.write(elboAngle-10)
     #         wrist.write(wristAngle+20)
      #        wristrotate.write(WristrotAngle)
       #3       gripper.write(GripperAngle-110)
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
     

    #IP webcam image stream 
    #URL = 'http://10.254.254.102:8080/shot.jpg'
    #urllib.urlretrieve(URL, 'shot1.jpg')
    #frame = cv2.imread('shot1.jpg')

 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=640,height=480)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 0.5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                print(x,y,key)       
                base.write(75+math.degrees(Cameraviewbase(x,y))) # Base view
                print(75+math.degrees(Cameraviewbase(x,y)))
                AngleCam = 75+math.degrees(Cameraviewbase(x,y))
                Settingfreeze(80,120,30,0,50)
                if key == "yellow":
                  if AngleCam >= 100:
                     if AngleCam <= 150: 
                       Settingfreeze(100,148,40,0,50)
                       time.sleep(1)
                       Settingfreeze(70,50,10,0,50)
                       time.sleep(1)
                       Settingfreeze(70,50,0,0,50)
                       time.sleep(1)
                       Settingfreeze(70,80,0,0,50)
                       time.sleep(1)
                       Settingfreeze(84,80,0,0,50)
                       time.sleep(1)
                       Settingfreeze(84,80,0,0,50)
                       time.sleep(3.1)
                       Settingfreeze(84,120,30,0,50)
                       gripper.write(50)
                  elif AngleCam < 90: 
                     Settingfreeze(80,120,30,0,50)
                #GripperWorks(key,120,120,20,0,50)
               

        
              #  elif(key != "blue"):
               #     if key != "green":
                #       base.write(75+math.degrees(Cameraviewbase(x,y))) # Base view
                 #      Settingfreeze(80,120,30,0,50)
         
                cv2.putText(frame,key + "cube", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)

     
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
