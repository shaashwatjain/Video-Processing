import speech_recognition as sr
import json

# For progressbar
import time
import spacy
import time
import progressbar
import os

path = os.getcwd() + "\\files"

widgets = [
    " [",
    progressbar.Timer(format="elapsed time: %(elapsed)s"),
    "] ",
    progressbar.Bar("*"),
    " (",
    progressbar.ETA(),
    ") ",
]

start = time.time()
try:
    file = open(os.getcwd() + "\\transcript_yt.txt", "r")
    count = 0
    L = []
    for line in file:
        L.append(line.strip())
        count += 1
    file.close()

    for i in range(0, count, 2):
        L[i] = "(" + L[i] + ")"
    M = L.copy()
    final = []
    for i in range(0, count, 2):
        final.append(L[i] + " " + M[i + 1])

    f = open(path + "\\transcript.txt", "w")
    for i in final:
        f.write(i)
        f.write("\n")
except:
    file_timing = open(path + "\\timings.txt", "r")
    timings = []
    timings = json.load(file_timing)
    file_timing.close()

    length = len(timings)

    bar = progressbar.ProgressBar(max_value=length, widgets=widgets).start()

    def dur(count):
        count = int(count)
        seconds = str(count % 60).zfill(2)
        minutes = str(int(count / 60)).zfill(2)
        return "(" + minutes + ":" + seconds + ")"

    count = 0
    i = 0
    r = sr.Recognizer()

    file_t = open(path + "\\transcript.txt", "w")

    import os

    my_path = os.getcwd() + "\\chunks"
    times = []

    while i < length - 1:
        filename = my_path + "\\chunk{0}.wav".format(i)
        str_time = dur(timings[i] / 1000)
        inner_start = time.time()
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data, language="en-US")
                temp = ""
                for letter in text:
                    temp += letter.lower()
                file_t.write(str_time + " " + temp + "\n")
            except:
                file_t.write(str_time + " " + "" + "\n")
        # print("--- %s seconds ---"% (time.time() - inner_start))
        times.append((time.time() - inner_start))
        if i < length:
            bar.update(i)
        i += 1

    file_t.close()
    print("Complete.")
    sum = 0
    for duration in times:
        sum += float(duration)
    print("--- %s seconds/transcription ---" % (sum / len(times)))
    print("--- %s seconds ---" % (time.time() - start))
