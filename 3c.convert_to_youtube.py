import os
path = os.getcwd() + '\\files'

file = open(path + '\\transcript_yt.txt','r')
count = 0
L=[]
for line in file:
    L.append(line.strip())
    count+=1
file.close()

for i in range(0,count,2):
    L[i]='('+L[i]+')'
M=L.copy()
final = []
for i in range(0,count,2):
    final.append(L[i]+' '+M[i+1])

f = open(path + '\\transcript.txt', 'w')
for i in final:
    f.write(i)
    f.write('\n')
