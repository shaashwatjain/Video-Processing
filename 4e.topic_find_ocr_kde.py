import spacy
import os

path = os.getcwd() + '\\files'

nlp = spacy.load('en_core_web_sm')

text = open(path + "\\ocr_transcript.txt",'r', encoding="utf-8").read()
list_sentences = text.split("\n")

synonyms = open(path + "\\synonyms.txt", 'r').read().split("\n")
synonyms.pop(-1)

pos_tagged = []
for sentence in list_sentences:
    doc = nlp(sentence)
    temp_tag = []
    for token in doc:
        temp_tag.append((token.text,token.tag_))
    pos_tagged.append(temp_tag)

list_sing = []
list_plu = []

for sentence in pos_tagged:
    for num,word_set in enumerate(sentence):
        if "NN" in word_set[1]:
            count = 1
            newstring = word_set[0]
            list_sing.append(newstring)
            while((num + count) < len(sentence) and ("NN" in sentence[num + count][1])):
                newstring += " " + sentence[num + count][0]
                count += 1
            if(count > 1):
                list_plu.append(newstring)
        if "JJ" in word_set[1]:
            count = 1
            newstring = word_set[0]
            while((num + count) < len(sentence) and ("JJ" in sentence[num + count][1])):
                newstring += " " + sentence[num + count][0]
                count += 1
            while((num + count) < len(sentence) and ("NN" in sentence[num + count][1])):
                newstring += " " + sentence[num + count][0]
                count += 1
            if("NN" in sentence[num + count - 1][1]):
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

imp_topics = []
for synonym in synonyms:
    for topic in list_plu:
        if synonym in topic:
            imp_topics.append(topic)

print("\nSynonym Derived Topics :")
for i in range(len(imp_topics)):
    print(imp_topics[i] + "\n")
    counted_plu[imp_topics[i]] += 1

from difflib import SequenceMatcher

def similarity(a,b):
    rat = SequenceMatcher(None,a,b).ratio()
    return float(rat)

to_delete = []
suffix = ['s','ing','ed']
for suf in suffix:
    for topic in counted_plu:
        if topic+suf in counted_plu:
            counted_plu[topic] += counted_plu[topic+suf]
            to_delete.append(topic+suf)

#print(to_delete)
for item in to_delete:
    del counted_plu[item]

to_delete = []
for topic in counted_plu:
    if topic not in to_delete:
        for check in counted_plu:
            if check != topic and check not in to_delete:
                if similarity(check,topic) > 0.85:
                    #print(check,topic)
                    if(counted_plu[check] > counted_plu[topic]):
                        to_delete.append(topic)
                        counted_plu[check] += counted_plu[topic]
                    else:
                        to_delete.append(check)
                        counted_plu[topic] += counted_plu[check]

#print(to_delete)
for item in set(to_delete):
    del counted_plu[item]


to_delete = []
for suf in suffix:
    for topic in counted_sing:
        if topic+suf in counted_sing:
            counted_sing[topic] += counted_sing[topic+suf]
            to_delete.append(topic+suf)

#print(to_delete)
for item in to_delete:
    del counted_sing[item]

counted_plu_export = dict()
counted_sing_export = dict()

import numpy as np
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt

plu_topic_val = list(counted_plu.values())

a = np.array(plu_topic_val).reshape(-1, 1)
#print(a)
kde = KernelDensity(kernel='gaussian', bandwidth=1).fit(a)
s = np.linspace(0,max(plu_topic_val))
e = kde.score_samples(s.reshape(-1,1))
plt.plot(s, e)
#plt.show()

print("\n\n\nTop Plural Topics :\n")
from scipy.signal import argrelextrema
mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
print ("Minima:", s[mi])
print ("Maxima:", s[ma])

threshold = None

if len(s[mi]) and len(s[ma]):
    threshold = (s[mi][0]+s[ma][0])/2
elif len(s[mi]):
    threshold = s[mi][0]
elif len(s[ma]):
    threshold = s[ma][0]
else:
    threshold = 0


for topic in counted_plu:
    if counted_plu[topic] > threshold:
        print(counted_plu[topic], topic)
        counted_plu_export[topic] = counted_plu[topic]


# sing_topic_val = list(counted_sing.values())

# a = np.array(sing_topic_val).reshape(-1, 1)
# #print(a)
# kde = KernelDensity(kernel='gaussian', bandwidth=1).fit(a)
# s = np.linspace(0,max(plu_topic_val))
# e = kde.score_samples(s.reshape(-1,1))
# plt.plot(s, e)
# #plt.show()


# print("\n\n\nTop Single Topics :\n")
# from scipy.signal import argrelextrema
# mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
# print ("Minima:", s[mi])
# print ("Maxima:", s[ma])

# if len(s[mi]) and len(s[ma]):
#     threshold = (s[mi][0]+s[ma][0])/2
# elif len(s[mi]):
#     threshold = s[mi][0]
# elif len(s[ma]):
#     threshold = s[ma][0]
# else:
#     threshold = 0

# for topic in counted_sing:
#     if counted_sing[topic] > threshold:
#         print(counted_sing[topic], topic)
#         counted_sing_export[topic] = counted_sing[topic]


import json
file_screen = open(path + "\\multiple_ocr.txt", "w")
json.dump(counted_plu_export, file_screen)
file_screen.close()
file_screen = open(path + "\\single_ocr.txt", "w")
json.dump(counted_sing, file_screen)
file_screen.close()