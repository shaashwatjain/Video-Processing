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

singular_words_file_full = open(path + "\\single_full.txt","r")
singular_words_full = dict()
singular_words_full = json.load(singular_words_file_full)
singular_words_file_full.close()
#print(singular_words)

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

import json
file_screen = open(path + "\\finalTopics_plu.txt", "w")
json.dump(list_plu_topics, file_screen)
file_screen.close()
file_screen = open(path + "\\finalTopics_sing.txt", "w")
json.dump(list(singular_topics.keys()), file_screen)
file_screen.close()