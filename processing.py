file = open('S:/Personal/video_proj/youtube_trans.txt','r')
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

f = open('S:/Personal/video_proj/transcript2.txt', 'w')
for i in final:
    f.write(i)
    f.write('\n')
