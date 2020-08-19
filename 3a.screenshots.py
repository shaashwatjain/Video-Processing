# Importing all necessary libraries
import cv2
import os
import time
import json
import send2trash

path = os.getcwd() + '\\files'
file_timing = open(path + "\\timings.txt","r")
timings = []
timings = json.load(file_timing)
print(timings)

# Read the video from specified path
cam = cv2.VideoCapture("video.mp4")

try:

    # creating a folder named data
    if not os.path.exists('captures'):
        os.makedirs('captures')
    else:
        send2trash.send2trash('captures')
        os.makedirs('captures')
    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 1000
i = 1
inc = len(timings)/100
if(inc < 1):
    inc = 1

while (i < len(timings)):
    currenttime = timings[i]
    cam.set(cv2.CAP_PROP_POS_MSEC, currenttime)
    i += int(inc)
    ret, frame = cam.read()
    
    if ret:
        # if video is still left continue creating images
        name = './captures/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)
        width = int(frame.shape[1] * 100/ 100)
        height = int(frame.shape[0] * 100/ 100)
        dim = (width, height)
        frame = cv2.resize(frame,dim,fx=0,fy=0, interpolation = cv2.INTER_AREA)
        # writing the extracted images
        cv2.imwrite(name, frame)

        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()