import os

path = os.getcwd() + "\\files"
file = open(path + "\\transcript_yt.txt", "r")

cnt, flag = 0, 0
content = []

for line in file:
    content.append(line.strip())
    if len(content[-1]) == 5 and ":" in content[-1]:
        if flag:
            content.insert(-1, " ")
            cnt += 1
            flag ^= 1
    cnt += 1
    flag ^= 1
file.close()

f = open(path + "\\transcript.txt", "w")
for i in range(0, cnt, 2):
    row = content[i] + " " + content[i + 1] + "\n"
    f.write("({}) {}\n".format(content[i], content[i + 1]))
