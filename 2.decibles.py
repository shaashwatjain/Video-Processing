# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
import speech_recognition as sr
from nltk.corpus import wordnet as wn
import time
import os
import send2trash

start = time.time()

# Load your audio.
song = AudioSegment.from_mp3("audio.mp3")

dBFS = song.dBFS
print(dBFS)

silences = detect_silence(
    song,
    min_silence_len = 550,
    silence_thresh = dBFS-10
)

#print(silences)

# Split track where the silence is 2 seconds or more and get chunks using 
# the imported function.
# chunks = split_on_silence(
#     # Use the loaded audio.
#     song, 
#     # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
#     min_silence_len = 550,
#     # Consider a chunk silent if it's quieter than -16 dBFS.
#     # (You may want to adjust this parameter.)
#     silence_thresh = dBFS-10,
#     keep_silence=550
# )

def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


# def dur(count):
#     count = int(count)
#     seconds = str(count % 60).zfill(2)
#     minutes = str(int(count / 60)).zfill(2)
#     return '(' + minutes + ':' + seconds + ')'

count = 0
# r = sr.Recognizer()

# file_t = open("sentence_transcribed.txt","w")

counted_duration = []

try:
    # creating a folder named data
    if not os.path.exists('chunks'):
        os.makedirs('chunks')
    else:
        send2trash.send2trash('chunks')
        os.makedirs('chunks')
    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# Process each chunk with your parameters
for i, chunk in enumerate(chunks):
    silence_chunk = AudioSegment.silent(duration=1000)

    # Add the padding chunk to beginning and end of the entire chunk.
    audio_chunk = silence_chunk + chunk + silence_chunk

    # Normalize the entire chunk.
    normalized_chunk = match_target_amplitude(audio_chunk, dBFS)
    # Export the audio chunk with new bitrate.
    print("Exporting chunk{0}.wav".format(i))
    filename = "chunks/chunk{0}.wav".format(i)
    normalized_chunk.export(
        filename,
        format = "wav"
    )
    # str_time = dur(count)
    # with sr.AudioFile(filename) as source:
    #     audio_data = r.record(source)
    #     try:
    #         text = r.recognize_google(audio_data, language="en-us")
    #         # meaningful = ""
    #         # for split in text.split():
    #         #     meaning = wn.synsets(split)
    #         #     if len(meaning) > 0:
    #         #         meaningful += split + " "
    #         temp = ""
    #         for letter in text:
    #             temp += letter.lower()
    #         file_t.write(str_time +" "+ temp + "\n")
    #     except:
    #         file_t.write(str_time +" " +"" + "\n")
    if i+1 < len(silences):
        counted_duration.append(count*1000)
        count = (silences[i+1][0]/1000)
counted_duration.append(count*1000)
#print(counted_duration)

import json
import os
path = os.getcwd() + '\files'
file_screen = open(path + "timings.txt", "w")
json.dump(counted_duration, file_screen)
file_screen.close()

print("--- %s seconds ---"% (time.time() - start))