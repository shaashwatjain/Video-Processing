import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import spacy
import os
path = os.getcwd() + '\\files'

nlp = spacy.load('en_core_web_sm')

text = open(path + "\\transcript.txt",'r').read()
tokenized_sentences = sent_tokenize(text)

synonyms = open(path + "\\synonyms.txt", 'r').read().split("\n")
synonyms.pop(-1)

list1 = []
list2 = []
imp_topics = []
   
position_tagged_t = []
temp_text = word_tokenize(text)
sentences = tokenized_sentences[0].split("\n")
for sentence in sentences:
    tags = nlp(sentence)
    temp_tag = [(word.text, word.tag_) for word in tags]
    for tag in temp_tag:
        position_tagged_t.append(tag)
#position_tagged_t = nltk.pos_tag(temp_text)
#print(position_tagged_t)
count = 0
for (num,(topic,type_t)) in enumerate(position_tagged_t):
    if "NN" in type_t or "JJ" in type_t:
        if(count > 0):
            count -= 1
        else:
            newstring = ""
            while((num + count < len(position_tagged_t)) and ("JJ" in position_tagged_t[num+count][1])):
                newstring = newstring + " " + position_tagged_t[num + count][0]
                count += 1
            if(not((num + count < len(position_tagged_t)) and ("NN" in position_tagged_t[num+count][1]))):
                count = 0
            while((num + count < len(position_tagged_t)) and ("NN" in position_tagged_t[num+count][1])):
                newstring = newstring + " " + position_tagged_t[num + count][0]
                count += 1
            if(count > 1):
                list1.append(newstring.lower())
            else:
                list2.append(newstring.lower())
            for word in synonyms:
                if count > 1:
                    for b_word in newstring.split(' '):
                        if word == b_word:
                            if newstring not in imp_topics:
                                imp_topics.append(newstring.lower())
    else:
        count = 0
        continue

counted_sing = dict()                
for word in set(list2):
    count = 0
    for match in list2:
        if word == match:
            count += 1
    counted_sing[word] = count


counted_plu = dict()                
for word in set(list1):
    count = 0
    for match in list1:
        if word == match:
            count += 1
    counted_plu[word] = count

#print(counted_plu)

print("Top Single Topics :")
singular = list(counted_sing.items())
singular.sort(key = lambda x:x[1],reverse=True)
#print(singular)

flag = 0
list_of_singwords=[]
if singular[0][1]==1:
    flag = 1
val = len(singular)%10
if val == 0 and len(singular)!=0:
    val = 10
    
#to change the topic freequency change the val
for key,count in singular[:val+10]:
    if count>1 and flag == 0:
        print(key,":" ,count)
        list_of_singwords.append(key)
    if flag == 1:
        print(key,":",count)

print("\nTop Plural Topics :")
plural = list(counted_plu.items())
plural.sort(key = lambda x:x[1],reverse = True)
#print(plural)

flag = 0
list_of_plurwords=[]
if plural[0][1]==1:
    flag = 1
val = len(singular)%10
if val == 0 and len(singular)!=0:
    val = 10


# To change the topic count change the val
for key,count in plural[:val+5]:
    if flag == 0 and count >=1:
        print(key,":",count)
        list_of_plurwords.append(key)
    if flag==1:
        print(key,":",count)

print("\nSynonym Derived Topics :")
for i in range(len(imp_topics)):
    print(imp_topics[i] + "\n")
    counted_plu[imp_topics[i]] += 1

print("\n")

print(list_of_singwords)
print(list_of_plurwords)

counted_plu_export = dict()
counted_sing_export = dict()

for topic in list_of_singwords:
    counted_sing_export[topic] = counted_sing[topic]

for topic in list_of_plurwords:
    counted_plu_export[topic] = counted_plu[topic]

import json
file_screen = open(path + "\\multiple.txt", "w")
json.dump(counted_plu_export, file_screen)
file_screen.close()
file_screen = open(path + "\\single.txt", "w")
json.dump(counted_sing, file_screen)
file_screen.close()