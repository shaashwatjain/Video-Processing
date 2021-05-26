# Importing all necessary libraries
import cv2
import os
import send2trash


def screenshoting(timings, videoname):
    """
    Takes arguments : timings, videoname
    Returns : nothing
    Exports : Captures in folder for ocr
    """
    print("Exporting OCR data")
    path = os.getcwd() + "\\files_" + videoname + "\\"

    # Read the video from specified path
    cam = cv2.VideoCapture(videoname + ".mp4")

    try:

        # creating a folder named data
        if not os.path.exists(path + "captures"):
            os.makedirs(path + "captures")
        else:
            send2trash.send2trash(path + "captures")
            os.makedirs(path + "captures")
        # if not created then raise error
    except OSError:
        print("Error: Creating directory of data")

    # frame
    currentframe = 1000
    i = 1
    inc = len(timings) / 50
    if inc < 1:
        inc = 1

    while i < len(timings):
        currenttime = timings[i]
        cam.set(cv2.CAP_PROP_POS_MSEC, currenttime)
        i += int(inc)
        ret, frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = (
                "./files_" + videoname + "/captures/frame" + str(currentframe) + ".jpg"
            )
            # print('Creating...' + name)
            width = int(frame.shape[1] * 100 / 100)
            height = int(frame.shape[0] * 100 / 100)
            dim = (width, height)
            frame = cv2.resize(frame, dim, fx=0, fy=0, interpolation=cv2.INTER_AREA)
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
    print("Exported OCR data")
