import cv2
import pytesseract
import json
import io
from nltk.corpus import wordnet as wn
import time
import spacy
import time
import progressbar

widgets = [
    " [",
    progressbar.Timer(format="elapsed time: %(elapsed)s"),
    "] ",
    progressbar.Bar("*"),
    " (",
    progressbar.ETA(),
    ") ",
]

nlp = spacy.load("en_core_web_sm")

start = time.time()

import os

path = os.getcwd() + "\\files"
file_timing = open(path + "\\timings.txt", "r")
timings = []
timings = json.load(file_timing)
file_timing.close()

length = len(timings)

bar = progressbar.ProgressBar(max_value=length, widgets=widgets).start()

inc = length / 100
if inc < 1:
    inc = 1


def dur(count):
    count = int(count)
    seconds = str(count % 60).zfill(2)
    minutes = str(int(count / 60)).zfill(2)
    return "(" + minutes + ":" + seconds + ")"


pytesseract.pytesseract.tesseract_cmd = (
    "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
)

my_path = os.getcwd() + "\\captures"

from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def similar_texts(text1, text2):
    ratio = similar(text1, text2)
    if ratio > 0.8:
        return True
    else:
        return False


complete_info = [""]
i = 1

ocr_data = io.open(path + "\\ocr_transcript.txt", "w", encoding="utf-8")

for folder, sub_folder, files in os.walk(my_path):
    for f in files:
        img = cv2.imread("captures/" + f)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(
            gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV
        )

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

        contours, hierarchy = cv2.findContours(
            dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        im2 = img.copy()
        info = []

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = im2[y : y + h, x : x + w]
            text = pytesseract.image_to_string(cropped)
            info.append(text)

        info_fin = []

        for text in info:
            if "\n" in text:
                text = text.replace("\n", " ")
            if text not in "":
                info_fin.append(text)

        tags = nlp(" ".join(info_fin))
        temp_tag = [(word.text, word.pos_) for word in tags]
        final_str = ""

        temp = []
        for (text, pos) in temp_tag:
            if pos in "NOUN":
                temp.append(text.lower())
            else:
                meaning = wn.synsets(text)
                if len(meaning) > 0:
                    temp.append(text.lower())
        if len(temp):
            final_str = " ".join(temp)
        # print(complete_info)

        if not similar_texts(final_str, complete_info[-1]):
            # print(final_str)
            if final_str != " ":
                ocr_data.write(dur(timings[i] / 1000) + " " + final_str + "\n")
            complete_info.append(final_str)
        i += int(inc)
        if i < length:
            bar.update(i)

ocr_data.close()
print("Complete.")
print("--- %s seconds ---" % (time.time() - start))
