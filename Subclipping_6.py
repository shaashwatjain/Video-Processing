import os
import sys
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from itertools import accumulate
from collections import defaultdict

def modifyTranscript(transcript):
    script = []
    for i in transcript:
        script.append(i.split())
    return script

def preprocessing(listOfPlurWords, transcript):
    # splitting the plural topics into individual words
    topics = set()
    for i in listOfPlurWords:
        for j in i.split():
            topics.add(j)

    # calculating the first occurence of the plural topics
    firstOccr = defaultdict(str)
    for i in listOfPlurWords:
        for line in transcript:
            if i in line:
                firstOccr[i] = [line.split()[0]]
                break
    return list(topics), firstOccr

def singleTopicsFinding(listOfWords, transcript):
    temp_dict = defaultdict(list)
    for i in listOfWords:
        tempList = []
        for j in transcript:
            if i in j:
                temp_dict[i].append(j[0])
    return temp_dict

def pluralTopicsFinding(listOfPlurWords, partialResultTopics):
    temp_dict = defaultdict(list)
    for topic in listOfPlurWords:
        tempSet = set()
        for i in topic.split():
            tempSet.update(partialResultTopics[i])
        tempSet = sorted(tempSet)
        temp_dict[topic] = tempSet
    return temp_dict

def convertTime(val):
    return sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(val.split(":"))))

def timeCalc(dictString):
    # Converting string time to second
    tempDict = defaultdict(list)
    for i,j in dictString.items():
        tempList=[]
        for k in j:
            k = k.strip('()')
            tempList.append(convertTime(k))
        tempDict[i]=tempList
    return tempDict

# starting the plural topics from the
def cleaningPluralTopics(secPluralTopics, secFirstOccr):
    for i, j in secPluralTopics.items():
        mark = secFirstOccr[i][0]
        while j[0] < mark:
            j.pop(0)
    return secPluralTopics

"""
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

"""
def subclipping(listOfSingWords, listOfPlurWords, mostOccuring, transcript):
    script = modifyTranscript(transcript)
    topics, firstOccr = preprocessing(listOfPlurWords, transcript)
    singleTopics = singleTopicsFinding(listOfSingWords, script)
    partialResultTopics = singleTopicsFinding(topics, script)
    pluralTopics = pluralTopicsFinding(listOfPlurWords, partialResultTopics)

    # converting the string time to sec
    secFirstOccr = timeCalc(firstOccr)
    secSingleTopics = timeCalc(singleTopics)
    secPluralTopics = timeCalc(pluralTopics)

    secPluralTopics = cleaningPluralTopics(secPluralTopics, secFirstOccr)
