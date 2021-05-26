"""
Building the foudation ranking system for topic finding.
Ranking to be taken into consideration:
Transcript (Single and Multiple) - 1/occurrence
Synonym Derived - +1/occurence
OCR verified - +1/occurrence
These values can be changed later according to results
Going to implement synonym in topic_find itself
"""

# Using two transcripts - Audio and OCR
import spacy

nlp = spacy.load("en_core_web_sm")
import numpy as np
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt


def delete_overlap(plural_words):
    to_delete = []
    for topic in plural_words:
        if topic not in to_delete:
            for check in plural_words:
                if check != topic and check not in to_delete:
                    if topic in check:
                        if plural_words[check] > plural_words[topic]:
                            to_delete.append(topic)
                            plural_words[check] += plural_words[topic]
                        else:
                            to_delete.append(check)
                            plural_words[topic] += plural_words[check]

    for item in set(to_delete):
        del plural_words[item]


def ocr_rank(text, singular_words, singular_words_ocr, plural_words_ocr):
    count = []
    topics = text.split()
    tag = nlp(text)
    for tagged in tag:
        if tagged.tag_ in "JJ":
            topics.remove(tagged.text)
    for topic in topics:
        if topic in singular_words_ocr:
            count.append(singular_words_ocr[topic])
        elif topic in singular_words:
            count.append(singular_words[topic])
        else:
            count.append(0)
    result1 = min(count)
    result = 0
    for plu_topic in plural_words_ocr:
        if text in plu_topic:
            # print(plu_topic)
            result2 = plural_words_ocr[plu_topic]
            if result2 > result:
                result = result2
    if not result:
        result = result1
    return result


def ranking(counted_plu, counted_sing, counted_sing_ocr, counted_plu_ocr):
    # print(counted_plu_ocr)
    delete_overlap(counted_plu)
    delete_overlap(counted_plu_ocr)
    # print(counted_plu)
    for topic, value in counted_plu.items():
        counted_plu[topic] = value + ocr_rank(
            topic, counted_sing, counted_sing_ocr, counted_plu_ocr
        )
    # print(counted_plu)
    most_occuring = finalise_topics(counted_plu)
    print("Ranking Complete")
    return most_occuring


def finalise_topics(list_topics):
    plu_topic_val = list(list_topics.values())

    a = np.array(plu_topic_val).reshape(-1, 1)
    kde = KernelDensity(kernel="gaussian", bandwidth=1).fit(a)
    s = np.linspace(0, max(plu_topic_val))
    e = kde.score_samples(s.reshape(-1, 1))
    plt.plot(s, e)
    # plt.show()

    from scipy.signal import argrelextrema

    mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
    # print ("Minima:", s[mi])
    # print ("Maxima:", s[ma])

    threshold = None

    if len(s[mi]) and len(s[ma]):
        threshold = (s[mi][0] + s[ma][0]) / 2
    elif len(s[mi]):
        threshold = s[mi][0]
    elif len(s[ma]):
        threshold = s[ma][0]
    else:
        threshold = 1

    # print('Threshold : ', threshold)
    most_occurring = None
    maxi = 0
    for topic in list_topics:
        if list_topics[topic] > threshold and list_topics[topic] > maxi:
            # print('Most occuring contender : ', topic)
            most_occurring = topic
            maxi = list_topics[topic]
    return most_occurring
