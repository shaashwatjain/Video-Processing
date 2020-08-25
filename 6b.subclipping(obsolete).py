from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from itertools import accumulate
import os
import json
path = os.getcwd() + '\\files'

#################################################### Loading files from external files

plural_topics_file = open(path + "\\finalTopics_plu.txt","r")
list_of_plurwords = []
list_of_plurwords = json.load(plural_topics_file)
plural_topics_file.close()

singular_topics_file = open(path + "\\finalTopics_sing.txt","r")
list_of_newwords = []
list_of_newwords = json.load(singular_topics_file)
singular_topics_file.close()

most_occurring = open(path + "\\most_occuring.txt","r")
most_occurring_topic = json.load(most_occurring)
most_occurring.close()

transcript_change = open(path + "\\singular_transcript.txt","r")
L = []
L = json.load(transcript_change)
transcript_change.close()

################################################# Files you'll need loaded 

topics=set()
for i in list_of_plurwords:
    for j in i.split():
        topics.add(j)
topics = list(topics)
topics.sort()

lines_text = []
for i in L:
    joined = " ".join(i)
    lines_text.append(joined)


limit = {}
for word in list_of_plurwords:
    arr=[]    
    for line in lines_text:
        if word in line:
            arr.append(line.split()[0])
    limit[word]=arr

#don't go below this
n =len(L)
final = {}
for j in topics:
    ans = []
    for i in range(n):
        if j in L[i]:
            #ans.append(i+1)
            ans.append(L[i][0])
    final[j]=ans
    
res = {}
for k in list_of_newwords:
    new = []
    for t in range(n):
        if k in L[t]:
            new.append(L[t][0])
    res[k] = new
    
result = {}
for i in list_of_plurwords:
    result[i]=set()


for i in list_of_plurwords:
    for j in i.split():
        result[i] = set(result[i]) | set(final[j])
        
    result[i] = list(result[i])
    result[i].sort()

"""
printing the result
for i,j in result.items():
    print(i,j)
"""    

def time_calc(result):
    time = list(result.items())
    time_diff={}
    FMT = '(%M:%S)'
    for i in time:
        diff=[]
        for j in range(len(i[1])):
            s1 = i[1][j]
            tdelta = datetime.strptime(s1, FMT)
            sec = (tdelta.minute*60)+tdelta.second
            diff.append(sec)
        k = i[0]
        time_diff[k]=diff
    return time_diff

def diff_calc(result):
    diff={}
    for i,j in result.items():  
        li=[]
        for k in range(len(j)-1):
            li.append(j[k+1]-j[k])
        diff[i]=li
    return diff


plural = time_calc(result)
single = time_calc(res)
together = time_calc(limit)

#starting the topic from where the two words together comes
for i in plural.keys():
    val = together[i][0]
    li = plural[i]
    for j in range(len(li)):
        if li[j]==val:
            plural[i] = li[j:]

to_be_deleted=[]
for i in plural.keys():
    if len(plural[i])==1:
        to_be_deleted.append(i)

pl = {}

for i in plural.keys():
    if i not in to_be_deleted:
        pl[i]=plural[i]

plural=pl
    

diff1=diff_calc(plural)
diff2=diff_calc(single)



def plot_box(result):
    labels=[]
    box_plot_data=[]
    answer = {}
    LEN = {}
    for i,j in result.items():
        s = np.array(j)
        LEN[i]=[0]
        box_plot_data.append(s)
        labels.append(i)
        median = np.median(s)
        upper_quartile = np.percentile(s, 75)
        lower_quartile = np.percentile(s, 25)
        iqr = upper_quartile - lower_quartile
        upper_whisker = s[s<=upper_quartile+1.5*iqr].max()
        #lower_whisker = j[j>=lower_quartile-1.5*iqr].min()
        #answer[i]=[lower_quartile,upper_quartile]
        #answer[i]=[lower_whisker,upper_quartile]
        count = 0
        for k in j:
            if k<=upper_whisker:
                count+=1
            else:
                LEN[i].append(count)
                count=1
        LEN[i].append(count)
                
    
    plt.boxplot(box_plot_data,vert = 0,labels=labels)
    #plt.show()
    #print(answer.items())
    return LEN

#plot_box(plural)
#plot_box(single)
plural.items()
diff1.items()
LEN = plot_box(diff1)    
#print(LEN)

new_len = {}
for i,j in LEN.items():
    L=list(accumulate(j))
    new_len[i]=L

#print(new_len.items())

"""
answer={}
for i,j in new_len.items():
    L=[]
    val = plural[i][0]
    for k in range(1,len(j)):
        lb = val
        val = sum(diff1[i][j[k-1]:j[k]])
        L.append([lb,val+lb])
        if j[k]!=j[-1]:
            val=plural[i][j[k]+1]
    answer[i]=L
"""
answer={}
for i,j in new_len.items():
    L=[]
    for k in range(1,len(j)):
        if j[k]-1 in j:
            continue
        if k==1:
            lb = plural[i][j[k-1]]
        else:
            lb = plural[i][j[k-1]+1]
        hb = plural[i][j[k]]
        L.append([lb,hb])
    if L!=[]:
        answer[i]=L

most_occurring_topic = ""
max_duration = 0
for topic in answer.keys():
    sum = 0
    for arr in answer[topic]:
        start_duration = arr[0]
        end_duration = arr[1]
        duration = end_duration - start_duration
        sum += duration
    if(sum > max_duration):
        max_duration = sum
        most_occurring_topic = topic


print(answer.items())
#print(plural.items())
print(most_occurring_topic)

# from moviepy.editor import *
# import os

# try:
#     if not os.path.exists(most_occurring_topic):
#         os.makedirs(most_occurring_topic)
#         print("Created Directory")
# except:
#     print("Error creating directory")

# for topic in answer.keys():
#     i = 1
#     for arr in answer[topic]:
#         start_duration = arr[0]
#         end_duration = arr[1]
#         if most_occurring_topic in topic:
#             continue
#         if(end_duration - start_duration > 10):
#             video = VideoFileClip("video.mp4").subclip(start_duration, end_duration)
#             video.write_videofile(most_occurring_topic + "/" + topic + str(i) +  ".mp4")
#         i += 1
        

