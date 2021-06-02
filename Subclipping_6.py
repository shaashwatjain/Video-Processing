import os

#  import matplotlib.pyplot as plt
import numpy as np

#  from datetime import datetime
from itertools import accumulate
from collections import defaultdict
from moviepy.editor import *


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
                tempList.append(j[0])
        if len(tempList) < 4:
            listOfWords.remove(i)
            continue
        temp_dict[i] = tempList
    return temp_dict


def pluralTopicsFinding(listOfPlurWords, partialResultTopics):
    temp_dict = defaultdict(list)
    for topic in listOfPlurWords:
        tempSet = set()
        for i in topic.split():
            tempSet.update(partialResultTopics[i])
        if len(tempSet) < 4:
            continue
        tempSet = sorted(tempSet)
        temp_dict[topic] = tempSet
    return temp_dict


def convertTime(val):
    return sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(val.split(":"))))


def timeCalc(argument):
    # Converting string time to second
    tempDict = defaultdict(list)
    for i, j in argument.items():
        tempList = []
        for k in j:
            k = k.strip("()")
            tempList.append(convertTime(k))
        tempDict[i] = tempList
    return tempDict


def cleaningPluralTopics(secPluralTopics, secFirstOccr):
    # starting the plural topics from the firstOccr
    tempDict = defaultdict(list)
    for i, j in secPluralTopics.items():
        mark = secFirstOccr[i][0]
        while j[0] < mark:
            j.pop(0)
        if len(j) > 3:
            tempDict[i] = j
    return tempDict


def diffCalc(argument):
    tempDict = defaultdict(list)
    for i, j in argument.items():
        tempList = []
        try:
            for k in range(len(j) - 1):
                tempList.append(j[k + 1] - j[k])
        except:
            print("Error in topic findings")
        tempDict[i] = tempList
    return tempDict


def timeDivision(argument):
    labels, boxPlotData = [], []
    tempDict = defaultdict(list)

    for i, j in argument.items():
        var = np.array(j)
        tempDict[i] = [0]
        boxPlotData.append(var)
        labels.append(i)
        median = np.median(var)
        upperQuartile = np.percentile(var, 75)
        lowerQuartile = np.percentile(var, 25)
        iqr = upperQuartile - lowerQuartile
        upperWhisker = var[var <= upperQuartile + 1.5 * iqr].max()
        cnt = 0
        for k in j:
            if k <= upperWhisker:
                cnt += 1
            else:
                tempDict[i].append(cnt)
                cnt = 1
        tempDict[i].append(cnt)
    # plt.boxplot(box_plot_data,vert = 0,labels=labels)
    return tempDict


def calcInterval(arg1, arg2):
    tempDict = defaultdict(list)
    for i, j in arg1.items():
        tempDict[i] = list(accumulate(j))

    answerDict = defaultdict(list)
    for i, j in tempDict.items():
        tempList = []
        for k in range(1, len(j)):
            if j[k] - 1 in j:
                continue
            if k == 1:
                lb = arg2[i][j[k - 1]]
            else:
                lb = arg2[i][j[k - 1] + 1]
            hb = arg2[i][j[k]]
            tempList.append([lb, hb])
        if tempList != []:
            answerDict[i] = tempList
    return answerDict


def convertSecToMin(timeSec):
    MIN = timeSec // 60
    SEC = timeSec % 60
    return str(MIN) + ":" + str(SEC)


def segmentVideo(mostOccuring, finalPluralTopics, videoname):
    mostOccurringTopic2 = ""
    maxDuration = 0
    for topic in finalPluralTopics.keys():
        total = 0
        for i in finalPluralTopics[topic]:
            startDuration, endDuration = i[0], i[1]
            total += endDuration - startDuration
        if total > maxDuration:
            maxDuration = total
            mostOccurringTopic2 = topic

    video = []
    debug = 0


    file = open("outputs.txt", 'a')
    if mostOccuring != mostOccurringTopic2:
        mostOccuring = mostOccurringTopic2
        # print(
        #     "Please choose your main topic(1/2):\n1. {}\n2. {}\n".format(
        #         mostOccuring, mostOccurringTopic2
        #     )
        # )

        # num = int(input("Enter here:"))
        # if num == 1:
        #     mostOccuring = mostOccuring
        # elif num == 2:
        #     mostOccuring = mostOccurringTopic2
        # else:
        #     print("Invalid option... Aborting")
        #     return 1

    del finalPluralTopics[mostOccuring]

    file.write(videoname + "\n")
    file.write(mostOccuring+":" + "\n")


    # try:
    #     if not os.path.exists("files_" + videoname + "/" + mostOccuring):
    #         os.makedirs("files_" + videoname + "/" + mostOccuring)
    #         print("Created Directory")
    # except:
    #     print("Error creating directory")

    for topic in finalPluralTopics.keys():
        file.write(topic + " - ")
        for i in finalPluralTopics[topic]:
            startDuration = i[0]
            endDuration = i[1]
            if mostOccuring in topic:
                continue
            if endDuration - startDuration > 10:
                video.append(
                    VideoFileClip(videoname+'.mp4').subclip(startDuration, endDuration)
                )
                file.write("("+convertSecToMin(startDuration)+", "+convertSecToMin(endDuration) + ")  ")
        file.write("\n")
        # print(video)
        if video and debug:
            finalClip = concatenate_videoclips(video)
            finalClip.write_videofile("files_" + videoname + "/"+ mostOccuring + "/" + topic + ".mp4")
            print("Written file :" + topic + "\n")
        video = []
    file.write("\n\n")
    file.close()
    return 0


def subclipping(listOfSingWords, listOfPlurWords, mostOccuring, transcript, videoname):
    script = modifyTranscript(transcript)
    singleTopics = singleTopicsFinding(listOfSingWords, script)
    topics, firstOccr = preprocessing(listOfPlurWords, transcript)
    partialResultTopics = singleTopicsFinding(topics, script)
    pluralTopics = pluralTopicsFinding(listOfPlurWords, partialResultTopics)

    # converting the string time to sec
    secFirstOccr = timeCalc(firstOccr)
    secSingleTopics = timeCalc(singleTopics)
    secPluralTopics = timeCalc(pluralTopics)

    secPluralTopics = cleaningPluralTopics(secPluralTopics, secFirstOccr)

    # converting diff between time
    diffPluralTopics = diffCalc(secPluralTopics)
    diffSingleTopics = diffCalc(secSingleTopics)

    lenPlural = timeDivision(diffPluralTopics)
    lenSingle = timeDivision(diffSingleTopics)

    finalPluralTopics = calcInterval(lenPlural, secPluralTopics)
    finalSingleTopics = calcInterval(lenSingle, secSingleTopics)

    segmentVideo(mostOccuring, finalPluralTopics, videoname)
