from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from itertools import accumulate
import os
import json

path = os.getcwd() + "\\files"

#################################################### Loading files from external files

plural_topics_file = open(path + "\\finalTopics_plu.txt", "r")
list_of_plurwords = []
list_of_plurwords = json.load(plural_topics_file)
plural_topics_file.close()

singular_topics_file = open(path + "\\finalTopics_sing.txt", "r")
list_of_newwords = []
list_of_newwords = json.load(singular_topics_file)
singular_topics_file.close()

most_occurring = open(path + "\\most_occuring.txt", "r")
most_occurring_topic = json.load(most_occurring)
most_occurring.close()

transcript_change = open(path + "\\singular_transcript.txt", "r")
script = []
script = json.load(transcript_change)
transcript_change.close()

###############################################################################

# splitting the plural topics into individual words
topics = set()
for i in list_of_plurwords:
    for j in i.split():
        topics.add(j)
topics = list(topics)
# print(topics)

# joing the transcript to search for the plural words
joined_script = []
for line in script:
    M = " ".join(line)
    joined_script.append(M)
# print(joined_script)

# claculating the first occurence of the plural topics
first_occr = {}
for i in list_of_plurwords:
    for line in joined_script:
        if i in line:
            first_occr[i] = [line.split()[0]]
            break
# print(first_occr.items())

################################################


def single_topics_finding(L):
    temp_dict = {}
    for i in L:
        li = []
        for j in script:
            if i in j:
                li.append(j[0])
        temp_dict[i] = li
    return temp_dict


single_topics = single_topics_finding(list_of_newwords)

partial_result = single_topics_finding(topics)
# print(partial_result.items())

plural_topics = {}
for topic in list_of_plurwords:
    li = set()
    for i in topic.split():
        li.update(partial_result[i])
    li = sorted(li)
    plural_topics[topic] = li
# print(plural_topics.items())


def time_calc(result):
    time = list(result.items())
    time_diff = {}
    FMT = "(%M:%S)"
    for i in time:
        diff = []
        for j in range(len(i[1])):
            s1 = i[1][j]
            tdelta = datetime.strptime(s1, FMT)
            sec = (tdelta.minute * 60) + tdelta.second
            diff.append(sec)
        k = i[0]
        time_diff[k] = diff
    return time_diff


# converting the string time to sec
sec_plural_topics = time_calc(plural_topics)
sec_first_occr = time_calc(first_occr)
sec_single_topics = time_calc(single_topics)
sec_topics_finding = time_calc(single_topics)

# starting the plural topics from the
for i, j in sec_plural_topics.items():
    print(i, j)
    mark = sec_first_occr[i][0]
    iter = 0
    while j[iter] < mark:
        j.pop(0)
# print(sec_plural_topics)


def diff_calc(result):
    diff = {}
    for i, j in result.items():
        li = []
        for k in range(len(j) - 1):
            li.append(j[k + 1] - j[k])
        diff[i] = li
    return diff


# converting diff between time
diff_plural_topics = diff_calc(sec_plural_topics)
diff_single_topics = diff_calc(sec_single_topics)


def time_division(result):
    labels = []
    box_plot_data = []
    LEN = {}
    for i, j in result.items():
        s = np.array(j)
        LEN[i] = [0]
        box_plot_data.append(s)
        labels.append(i)
        median = np.median(s)
        upper_quartile = np.percentile(s, 75)
        lower_quartile = np.percentile(s, 25)
        iqr = upper_quartile - lower_quartile
        upper_whisker = s[s <= upper_quartile + 1.5 * iqr].max()
        count = 0
        for k in j:
            if k <= upper_whisker:
                count += 1
            else:
                LEN[i].append(count)
                count = 1
        LEN[i].append(count)
    # plt.boxplot(box_plot_data,vert = 0,labels=labels)
    return LEN


LEN_plural = time_division(diff_plural_topics)
LEN_single = time_division(diff_single_topics)


def calc_interval(LEN, result):
    new_len = {}
    for i, j in LEN.items():
        L = list(accumulate(j))
        new_len[i] = L

    answer = {}
    for i, j in new_len.items():
        L = []
        for k in range(1, len(j)):
            if j[k] - 1 in j:
                continue
            if k == 1:
                lb = result[i][j[k - 1]]
            else:
                lb = result[i][j[k - 1] + 1]
            hb = result[i][j[k]]
            L.append([lb, hb])
        if L != []:
            answer[i] = L
    return answer


final_plural_topics = calc_interval(LEN_plural, sec_plural_topics)
final_single_topics = calc_interval(LEN_single, sec_single_topics)
print(final_plural_topics.items())
print(final_single_topics.items())

most_occurring_topic2 = ""
max_duration = 0
for topic in final_plural_topics.keys():
    sum = 0
    for arr in final_plural_topics[topic]:
        start_duration = arr[0]
        end_duration = arr[1]
        duration = end_duration - start_duration
        sum += duration
    if sum > max_duration:
        max_duration = sum
        most_occurring_topic2 = topic

video = []
abort = 0
if not most_occurring_topic == most_occurring_topic2:
    print(
        "Please choose your main topic(1/2):\n1. "
        + most_occurring_topic
        + "\n2. "
        + most_occurring_topic2
        + "\n"
    )
    num = int(input("Enter here:"))
    if num == 1:
        most_occurring_topic = most_occurring_topic
        abort = 0
    elif num == 2:
        most_occurring_topic = most_occurring_topic2
        abort = 0
    else:
        print("Invalid option... Aborting")
        abort = 1

if not abort:
    from moviepy.editor import *

    try:
        if not os.path.exists(most_occurring_topic):
            os.makedirs(most_occurring_topic)
            print("Created Directory")
    except:
        print("Error creating directory")

    for topic in final_plural_topics.keys():
        for arr in final_plural_topics[topic]:
            start_duration = arr[0]
            end_duration = arr[1]
            if most_occurring_topic in topic:
                continue
            if end_duration - start_duration > 10:
                video.append(
                    VideoFileClip("video.mp4").subclip(start_duration, end_duration)
                )
        finalClip = concatenate_videoclips(video)
        finalClip.write_videofile(most_occurring_topic + "/" + topic + ".mp4")
        print("Written file :" + topic)
