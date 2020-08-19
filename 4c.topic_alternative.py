import spacy
import os
path = os.getcwd() + '\\files'

nlp = spacy.load('en_core_web_sm')

text = open(path + "\\transcript.txt",'r').read()
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

imp_topics = []
for synonym in synonyms:
    for topic in list_plu:
        if synonym in topic:
            imp_topics.append(topic)

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
file_screen = open(path + "\\single_full.txt", "w")
json.dump(counted_sing, file_screen)
file_screen = open(path + "\\single.txt", "w")
json.dump(counted_sing_export, file_screen)
file_screen.close()