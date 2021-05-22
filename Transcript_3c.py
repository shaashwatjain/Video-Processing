import speech_recognition as sr
import json
import progressbar
import os
import time
import sys


def dur(count):
    count = int(count)
    seconds = str(count % 60).zfill(2)
    minutes = str(int(count / 60)).zfill(2)
    return "(" + minutes + ":" + seconds + ")"


def isTimeFormat(value):
    try:
        time.strptime(value, "%M:%S")
        return True
    except ValueError:
        return False


def transcript(timings, videoname):

    path = os.getcwd() + "\\files_" + videoname + "\\"

    widgets = [
        " [",
        progressbar.Timer(format="elapsed time: %(elapsed)s"),
        "] ",
        progressbar.Bar("*"),
        " (",
        progressbar.ETA(),
        ") ",
    ]

    try:
        file = open(os.getcwd() + "\\" + videoname + ".txt", "r")

        cnt, flag = 0, 0
        content = []

        for line in file:
            row = line.strip()
            if isTimeFormat(row):
                if flag:
                    content.pop(-1)
                    cnt -= 1
                else:
                    flag = 1

            else:
                if not flag:
                    continue
                flag = 0
                if row == "" and cnt > 1:
                    content.pop(-1)
                    cnt -= 1
                    continue
            content.append(row)
            cnt += 1

        if flag == 1 and content:
            content.pop(-1)
            cnt -= 1
        file.close()

        transcript = []
        for i in range(0, cnt, 2):
            row = content[i] + " " + content[i + 1] + "\n"
            transcript.append("({}) {}".format(content[i], content[i + 1]))

        print("\nExported Speech Transcript")
        return transcript

    except:
        length = len(timings)

        bar = progressbar.ProgressBar(max_value=length, widgets=widgets).start()

        count = 0
        i = 0
        r = sr.Recognizer()
        my_path = path + "chunks\\"
        transcript = []

        while i < length - 1:
            filename = my_path + "chunk{0}.wav".format(i)
            str_time = dur(timings[i] / 1000)
            with sr.AudioFile(filename) as source:
                r.adjust_for_ambient_noise(source)
                audio_data = r.record(source)
                try:
                    text = r.recognize_google(audio_data, language="en-US")
                    temp = ""
                    for letter in text:
                        temp += letter.lower()
                    transcript.append(str_time + " " + temp)
                except:
                    transcript.append(str_time + " " + "")
            if i < length:
                bar.update(i)
            i += 1
        bar.update(i)
        print("\nExported Speech Transcript")
        return transcript


# data = transcript([0, 1714.0, 4105.0, 6836.0, 8685.0, 14273.0, 17333.0, 22977.0, 28297.0, 33579.0, 36558.0, 38914.0, 42499.0, 49050.0, 53589.0, 59859.0, 64474.99999999999, 73405.0, 77626.0, 84316.0, 89617.0]
#     ,'temp')
# print(data)
