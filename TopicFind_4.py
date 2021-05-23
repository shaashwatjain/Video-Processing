import spacy
import numpy as np
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
from difflib import SequenceMatcher

nlp = spacy.load('en_core_web_sm')

def spacy_process(text, pos_tagged):
    doc = nlp(text)
    lemma = ""
    temp_tag = []
    for token in doc:
        temp_lemma = token.lemma_
        if temp_lemma == '-PRON-':
            temp_lemma = token.text
        temp_lemma = temp_lemma.lower()
        lemma += temp_lemma + ' '
        temp_tag.append((temp_lemma,token.tag_))
    pos_tagged.append(temp_tag)
    return lemma

def convert_transcript(transcript, pos_tagged):
    for num,line in enumerate(transcript):
        transcript[num] = line[:8] + spacy_process(line[8:], pos_tagged)
    # print(transcript)

def topic_find(transcript, counted_sing = dict(), counted_plu = dict()):
    # print(counted_plu)
    pos_tagged = []
    convert_transcript(transcript, pos_tagged)
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
             
    for word in set(list_sing):
        count = 0
        for match in list_sing:
            if word == match:
                count += 1
        counted_sing[word] = count

               
    for word in set(list_plu):
        count = 0
        for match in list_plu:
            if word == match:
                count += 1
        counted_plu[word] = count
    
    # print(counted_plu)
    
    similarity_removal(counted_sing)
    similarity_removal(counted_plu)

    # print(counted_plu)

    if counted_sing:
        display_topics(counted_sing)
    if counted_plu:
        display_topics(counted_plu)

    print('Found Topics')

    return (counted_sing,counted_plu)


def display_topics(counted_list):
    topic_val = list(counted_list.values())

    a = np.array(topic_val).reshape(-1, 1)
    #print(a)
    kde = KernelDensity(kernel='gaussian', bandwidth=1).fit(a)
    s = np.linspace(0,max(topic_val))
    e = kde.score_samples(s.reshape(-1,1))
    plt.plot(s, e)
    #plt.show()

    # print("\nTop Topics :\n")
    from scipy.signal import argrelextrema
    mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
    # print ("Minima:", s[mi])
    # print ("Maxima:", s[ma])

    threshold = None

    if len(s[mi]) and len(s[ma]):
        threshold = (s[mi][0]+s[ma][0])/2
    elif len(s[mi]):
        threshold = s[mi][0]
    elif len(s[ma]):
        threshold = s[ma][0]
    else:
        threshold = 0

    topics = []
    for topic in counted_list:
        if counted_list[topic] >= float(threshold):
            # print(counted_list[topic], topic)
            pass
        else:
            topics.append(topic)
    for topic in topics:
        del counted_list[topic]


def similarity(a,b):
    rat = SequenceMatcher(None,a,b).ratio()
    return float(rat)

def similarity_removal(counted_list):
    to_delete = []
    for topic in counted_list:
        if topic not in to_delete:
            for check in counted_list:
                if check != topic and check not in to_delete:
                    if similarity(check,topic) > 0.85:
                        if(counted_list[check] > counted_list[topic]):
                            to_delete.append(topic)
                            counted_list[check] += counted_list[topic]
                        else:
                            to_delete.append(check)
                            counted_list[topic] += counted_list[check]

    #print(to_delete)
    for item in set(to_delete):
        del counted_list[item]
