'''
Building the foudation ranking system for topic finding.
Ranking to be taken into consideration:
Transcript (Single and Multiple) - 1/occurrence
Synonym Derived - +1/occurence
OCR verified - +1/occurrence
These values can be changed later according to results
Going to implement synonym in topic_find itself
'''

# Using two transcripts - Audio and OCR

import json
import os
path = os.getcwd() + '\\files'

plural_words_file = open(path + "\\multiple.txt","r")
plural_words = dict()
plural_words = json.load(plural_words_file)
plural_words_file.close()
#print(plural_words)

singular_words_file = open(path + "\\single.txt","r")
singular_words = dict()
singular_words = json.load(singular_words_file)
singular_words_file.close()

plural_words_ocr = dict()
singular_words_ocr = dict()
try:    
    plural_words_file_ocr = open(path + "\\multiple_ocr.txt","r")
    plural_words_ocr = json.load(plural_words_file_ocr)
    plural_words_file_ocr.close()
    #print(plural_words_ocr)

    singular_words_file_ocr = open(path + "\\single_ocr.txt","r")
    singular_words_ocr = json.load(singular_words_file_ocr)
    singular_words_file_ocr.close()
    #print(singular_words_ocr)
except:
    print("No OCR transcript generated")

plural_topics = dict()
singular_topics = dict()

def ocr_rank(text):
    count = []
    topics = text.split()
    for topic in topics:
        if topic in singular_words_ocr:
            count.append(singular_words_ocr[topic])
        else:
            count.append(0)
    result = min(count)
    if text in plural_words_ocr:
        result = plural_words_ocr[text]
    return result

for topic,value in plural_words.items():
    plural_topics[topic] = value + ocr_rank(topic)

print(plural_topics)

for topic,value in singular_words.items():
    singular_topics[topic] = value + ocr_rank(topic)

print(singular_topics)

import numpy as np
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt

plu_topic_val = list(plural_topics.values())

a = np.array(plu_topic_val).reshape(-1, 1)
#print(a)
kde = KernelDensity(kernel='gaussian', bandwidth=1).fit(a)
s = np.linspace(0,max(plu_topic_val))
e = kde.score_samples(s.reshape(-1,1))
plt.plot(s, e)
#plt.show()

from scipy.signal import argrelextrema
mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
print ("Minima:", s[mi])
print ("Maxima:", s[ma])

plural_topics_export = dict()
singular_topics_export = dict()

threshold = None

if len(s[mi]) and len(s[ma]):
    threshold = (s[mi][0]+s[ma][0])/2
elif len(s[mi]):
    threshold = s[mi][0]
elif len(s[ma]):
    threshold = s[ma][0]
else:
    threshold = 1

maxi = 0
most_occurring = None
for topic in plural_topics:
    if plural_topics[topic] > threshold:
        print(plural_topics[topic], topic)
        plural_topics_export[topic] = plural_topics[topic]
        if plural_topics[topic] > maxi:
            maxi = plural_topics[topic]
            most_occurring = topic

sorted_a = list(plural_topics_export.keys())
sorted_a.sort()

for i,check in enumerate(sorted_a):
    if sorted_a[i - 1] in check:
        del plural_topics_export[sorted_a[i-1]]

sing_topic_val = list(singular_topics.values())

a = np.array(sing_topic_val).reshape(-1, 1)
#print(a)
kde = KernelDensity(kernel='gaussian', bandwidth=1).fit(a)
s = np.linspace(0,max(sing_topic_val))
e = kde.score_samples(s.reshape(-1,1))
plt.plot(s, e)
#plt.show()

from scipy.signal import argrelextrema
mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
print ("Minima:", s[mi])
print ("Maxima:", s[ma])


if len(s[mi]) > 1 and len(s[ma]) > 1:
    threshold = (s[mi][-2]+s[ma][-2])/2
elif len(s[mi]):
    threshold = s[mi][-1]
elif len(s[ma]):
    threshold = s[ma][-1]
else:
    threshold = 1


for topic in singular_topics:
    if singular_topics[topic] > threshold:
        print(singular_topics[topic], topic)
        singular_topics_export[topic] = singular_topics[topic]



import json
file_screen = open(path + "\\finalTopics_plu.txt", "w")
json.dump(list(plural_topics_export.keys()), file_screen)
file_screen.close()
file_screen = open(path + "\\finalTopics_sing.txt", "w")
json.dump(list(singular_topics_export.keys()), file_screen)
file_screen.close()
file_screen = open(path + "\\most_occuring.txt", "w")
json.dump(most_occurring, file_screen)
file_screen.close()