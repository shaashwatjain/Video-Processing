# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import detect_silence
import speech_recognition as sr
from nltk.corpus import wordnet as wn
import send2trash
import os


def chunking_audio(videoname):
    """
    return timings
    """

    print("Exporting chunks ...")

    path = os.getcwd() + "\\files_" + videoname + "\\"

    # Load your audio.
    song = AudioSegment.from_wav(path + "\\audio.wav")

    try:
        # creating a folder named data
        if not os.path.exists(path + "chunks"):
            os.makedirs(path + "chunks")
        else:
            send2trash.send2trash(path + "chunks")
            os.makedirs(path + "chunks")
        # if not created then raise error
    except OSError:
        print("Error: Creating directory of data")

    dBFS = song.dBFS

    silences = detect_silence(song, min_silence_len=550, silence_thresh=dBFS - 10)

    # print(silences)

    def match_target_amplitude(aChunk, target_dBFS):
        """Normalize given audio chunk"""
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)

    count = 0
    counted_duration = []
    i = 0

    # Process each chunk with your parameters
    while i + 1 < len(silences):
        chunk = song[silences[i][0] + 50 : silences[i + 1][1] - 50]

        silence_chunk = AudioSegment.silent(duration=1000)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, dBFS)
        # Export the audio chunk with new bitrate.
        # print("Exporting chunk{0}.wav".format(i))
        filename = "files_" + videoname + "/chunks/chunk{0}.wav".format(i)
        normalized_chunk.export(filename, format="wav")

        if i + 1 < len(silences):
            counted_duration.append(count * 1000)
            count = silences[i + 1][0] / 1000
        i += 1

    counted_duration.append(count * 1000)
    print("Exported chunks")

    return counted_duration
