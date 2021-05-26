import moviepy.editor as mp
import os
import send2trash


def export_files_and_audio(videoname):
    """
    exports synonyms and also audio in wav format for further processes
    """

    path = os.getcwd() + "\\files_" + videoname

    clip = mp.VideoFileClip(videoname + ".mp4")
    clip.audio.write_audiofile(path + "\\audio.wav")

    synonyms = open(path + "\\synonyms.txt", "w")
    synonyms.write("course\nsubject\ntheorem")
    synonyms.close()
