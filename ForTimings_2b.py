from datetime import datetime
import re

def timings(videoname):
    transcript_path = videoname + ".txt"
    f = open(transcript_path, "r")
    timings = [0.0]
    for text in f:
        text = text.strip()
        mat = re.match('\d{2}:\d{2}',text)
        # print(text, mat)
        if mat:
            x = datetime.strptime(text, "%M:%S")
            timings.append(float(x.minute * 60 * 1000 + x.second * 1000))
    # print(timings)
    return timings