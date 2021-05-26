from datetime import datetime


def timings(videoname):
    transcript_path = videoname + ".txt"
    f = open(transcript_path, "r")
    timings = [0.0]
    text = f.readline().strip()
    while text:
        x = datetime.strptime(text, "%M:%S")
        timings.append(float(x.minute * 60 * 1000 + x.second * 1000))
        f.readline().strip()
        text = f.readline().strip()
    return timings
