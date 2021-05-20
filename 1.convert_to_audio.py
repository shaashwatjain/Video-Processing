import moviepy.editor as mp
import os
import send2trash

try:
    # creating a folder named data
    if not os.path.exists("files"):
        os.makedirs("files")
    else:
        send2trash.send2trash("files")
        os.makedirs("files")
    # if not created then raise error
except OSError:
    print("Error: Creating directory of data")

path = os.getcwd() + "\\files"

clip = mp.VideoFileClip("video.mp4")
clip.audio.write_audiofile(path + "\\audio.wav")

synonyms = open(path + "\\synonyms.txt", "w")
synonyms.write("course\nsubject\ntheorem")
synonyms.close()
