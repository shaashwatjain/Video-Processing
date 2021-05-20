import spacy
import os
import json

path = os.getcwd() + "\\files"

nlp = spacy.load("en_core_web_sm")

text = open(path + "\\transcript.txt", "r").read()
list_sentences = text.split("\n")

synonyms = open(path + "\\synonyms.txt", "r").read().split("\n")
synonyms.pop(-1)

pos_tagged = []
for sentence in list_sentences:
    doc = nlp(sentence)
    temp_tag = []
    for token in doc:
        temp_tag.append((token.text, token.tag_))
    pos_tagged.append(temp_tag)

list_sing = []
list_plu = []

for sentence in pos_tagged:
    for num, word_set in enumerate(sentence):
        if "NN" in word_set[1]:
            count = 1
            newstring = word_set[0]
            list_sing.append(newstring)
            while (num + count) < len(sentence) and ("NN" in sentence[num + count][1]):
                newstring += " " + sentence[num + count][0]
                count += 1
            if count > 1:
                list_plu.append(newstring)
        if "JJ" in word_set[1]:
            count = 1
            newstring = word_set[0]
            while (num + count) < len(sentence) and ("JJ" in sentence[num + count][1]):
                newstring += " " + sentence[num + count][0]
                count += 1
            while (num + count) < len(sentence) and ("NN" in sentence[num + count][1]):
                newstring += " " + sentence[num + count][0]
                count += 1
            if "NN" in sentence[num + count - 1][1]:
                list_plu.append(newstring)

counted_sing = dict()
for word in set(list_sing):
    count = 0
    for match in list_sing:
        if word == match:
            count += 1
    counted_sing[word] = count


counted_plu = dict()
for word in set(list_plu):
    count = 0
    for match in list_plu:
        if word == match:
            count += 1
    counted_plu[word] = count

############################################## Changes for 6.subclipping

list_of_singwords = list(counted_sing.keys())
list_of_morewords = list(counted_plu.keys())

list_of_newwords = []
for i in list_of_singwords:
    j = i.strip()
    list_of_newwords.append(j)

list_of_plurwords = []
for i in list_of_morewords:
    j = i.strip()
    list_of_plurwords.append(j)

topics = set()

for i in list_of_plurwords:
    for j in i.split():
        if j in list_of_newwords:
            list_of_newwords.remove(j)
        topics.add(j)
topics = list(topics)
topics.sort()

pos = []
duplicate = []
true = []
suffix = ["s", "ed"]
for i in range(len(topics) - 1):
    for j in suffix:
        if topics[i] + j == topics[i + 1]:
            pos.append(i + 1)
            duplicate.append(topics[i + 1])
            true.append(topics[i])

# removing plural words from topics
count = 0
for i in pos:
    topics.pop(i - count)
    count += 1

list_of_plurwords.sort()
for j in duplicate:
    for i in list_of_plurwords:
        if j in i:
            list_of_plurwords.remove(i)

imp_topics = []
for synonym in synonyms:
    for topic in list_plu:
        if synonym in topic:
            imp_topics.append(topic)

print("\nSynonym Derived Topics :")
for i in range(len(imp_topics)):
    print(imp_topics[i] + "\n")
    counted_plu[imp_topics[i]] += 1


file = open(path + "\\transcript.txt", "r")
line = file.readline()

L = []
while line:
    M = []
    # print(line)
    for word in line.split():
        if word in duplicate:
            for k in range(len(duplicate)):
                if duplicate[k] == word:
                    word = true[k]
        M.append(word.lower())
    L.append(M)
    line = file.readline()
file.close()

file_screen = open(path + "\\singular_transcript.txt", "w")
json.dump(L, file_screen)
file_screen.close()

############################################ Changes for 6.subclipping

from difflib import SequenceMatcher


def similarity(a, b):
    rat = SequenceMatcher(None, a, b).ratio()
    return float(rat)


to_delete = []
suffix = ["s", "ed"]
for suf in suffix:
    for topic in counted_plu:
        if topic + suf in counted_plu:
            counted_plu[topic] += counted_plu[topic + suf]
            to_delete.append(topic + suf)

# print(to_delete)
for item in to_delete:
    del counted_plu[item]

to_delete = []
for topic in counted_plu:
    if topic not in to_delete:
        for check in counted_plu:
            if check != topic and check not in to_delete:
                if similarity(check, topic) > 0.85:
                    # print(check,topic)
                    if counted_plu[check] > counted_plu[topic]:
                        to_delete.append(topic)
                        counted_plu[check] += counted_plu[topic]
                    else:
                        to_delete.append(check)
                        counted_plu[topic] += counted_plu[check]

# print(to_delete)
for item in set(to_delete):
    del counted_plu[item]


to_delete = []
for suf in suffix:
    for topic in counted_sing:
        if topic + suf in counted_sing:
            counted_sing[topic] += counted_sing[topic + suf]
            to_delete.append(topic + suf)

# print(to_delete)
for item in to_delete:
    del counted_sing[item]

to_delete = []
for topic in counted_sing:
    if topic not in to_delete:
        for check in counted_sing:
            if check != topic and check not in to_delete:
                if similarity(check, topic) > 0.85:
                    if counted_sing[check] > counted_sing[topic]:
                        to_delete.append(topic)
                        counted_sing[check] += counted_sing[topic]
                    else:
                        to_delete.append(check)
                        counted_sing[topic] += counted_sing[check]

# print(to_delete)
for item in set(to_delete):
    del counted_sing[item]

counted_plu_export = dict()
counted_sing_export = dict()

import numpy as np
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt

plu_topic_val = list(counted_plu.values())

a = np.array(plu_topic_val).reshape(-1, 1)
# print(a)
kde = KernelDensity(kernel="gaussian", bandwidth=1).fit(a)
s = np.linspace(0, max(plu_topic_val))
e = kde.score_samples(s.reshape(-1, 1))
plt.plot(s, e)
# plt.show()

print("\nTop Plural Topics :\n")
from scipy.signal import argrelextrema

mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
print("Minima:", s[mi])
print("Maxima:", s[ma])

threshold = None

if len(s[mi]) and len(s[ma]):
    threshold = (s[mi][0] + s[ma][0]) / 2
elif len(s[mi]):
    threshold = s[mi][0]
elif len(s[ma]):
    threshold = s[ma][0]
else:
    threshold = 0


for topic in counted_plu:
    if counted_plu[topic] >= float(threshold):
        print(counted_plu[topic], topic)
        counted_plu_export[topic] = counted_plu[topic]


sing_topic_val = list(counted_sing.values())

a = np.array(sing_topic_val).reshape(-1, 1)
# print(a)
kde = KernelDensity(kernel="gaussian", bandwidth=1).fit(a)
s = np.linspace(0, max(sing_topic_val))
e = kde.score_samples(s.reshape(-1, 1))
plt.plot(s, e)
# plt.show()


print("\nTop Single Topics :\n")
from scipy.signal import argrelextrema

mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
print("Minima:", s[mi])
print("Maxima:", s[ma])

if len(s[mi]) and len(s[ma]):
    threshold = (s[mi][0] + s[ma][0]) / 2
elif len(s[mi]):
    threshold = s[mi][0]
elif len(s[ma]):
    threshold = s[ma][0]
else:
    threshold = 0

for topic in counted_sing:
    if counted_sing[topic] > threshold:
        print(counted_sing[topic], topic)
        counted_sing_export[topic] = counted_sing[topic]


file_screen = open(path + "\\multiple.txt", "w")
json.dump(counted_plu_export, file_screen)
file_screen.close()
file_screen = open(path + "\\single.txt", "w")
json.dump(counted_sing_export, file_screen)
file_screen.close()
