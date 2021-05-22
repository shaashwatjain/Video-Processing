import os
import sys
import time


path = os.getcwd() + "\\files"
file = open(path + "\\transcript_yt.txt", "r")
full_path = path + "\\transcript_yt.txt"

cnt, flag = 0, 0
content = []

#  if os.stat(full_path).st_size == 0:
#      print("Already present transcript is empty...")

def isTimeFormat(value):
    try:
        time.strptime(value, '%M:%S')
        return True
    except ValueError:
        return False

for line in file:
    row = line.strip()
    if isTimeFormat(row):
        if flag:
            content.pop(-1)
            cnt-=1
        else:
            flag=1

    else:
        if not flag:
            continue
        flag = 0
        if row=="" and cnt>1:
            content.pop(-1)
            cnt-=1
            continue
    content.append(row)
    cnt+=1

if flag==1 and content:
    content.pop(-1)
    cnt-=1
file.close()

f = open(path + "\\transcript.txt", "w")
#  if cnt<2:
#      print("Transcript is not correct")
#      sys.exit()

for i in range(0, cnt, 2):
    row = content[i] + " " + content[i + 1] + "\n"
    f.write("({}) {}\n".format(content[i], content[i + 1]))
