import ConvertToAudio_1 as convert
import Chunking_2 as chunking
import ForTimings_2b as Timings
import Screenshots_3a as screenshots
import OCRTranscript_3b as OCR
import Transcript_3c as trans
import TopicFind_4 as Topic
import Ranking_5 as Ranking
import Subclipping_6 as Subclipping
import os
import send2trash


def runFull(videoname, counted_sing, counted_sing_ocr, counted_plu, counted_plu_ocr):
    convert.export_files_and_audio(videoname)
    timings = chunking.chunking_audio(videoname)
    screenshots.screenshoting(timings, videoname)
    ocr_transcript = OCR.ocr_gen(timings, videoname)
    transcript = trans.transcript(timings, videoname)

    (counted_sing, counted_plu) = Topic.topic_find(
        transcript, counted_sing, counted_plu
    )

    (counted_sing_ocr, counted_plu_ocr) = Topic.topic_find(
        ocr_transcript, counted_sing_ocr, counted_plu_ocr
    )

    most_occuring = Ranking.ranking(
        counted_plu, counted_sing, counted_sing_ocr, counted_plu_ocr
    )

    #  print(counted_plu)
    Subclipping.subclipping(
        list(counted_sing.keys()), list(counted_plu.keys()), most_occuring, transcript, videoname
    )
    #  return most_occuring


def runWithTranscript(
    videoname, counted_sing, counted_sing_ocr, counted_plu, counted_plu_ocr
):
    timings = Timings.timings(videoname)
    screenshots.screenshoting(timings, videoname)
    ocr_transcript = OCR.ocr_gen(timings, videoname)
    # print(ocr_transcript)
    transcript = trans.transcript(timings, videoname)
    (counted_sing, counted_plu) = Topic.topic_find(
        transcript, counted_sing, counted_plu
    )

    (counted_sing_ocr, counted_plu_ocr) = Topic.topic_find(
        ocr_transcript, counted_sing_ocr, counted_plu_ocr
    )

    most_occuring = Ranking.ranking(
        counted_plu, counted_sing, counted_sing_ocr, counted_plu_ocr
    )

    #  print(counted_plu)
    Subclipping.subclipping(
        list(counted_sing.keys()), list(counted_plu.keys()), most_occuring, transcript, videoname
    )


files = []
transcripts = []

for (folder, subfolder, file) in os.walk("./"):
    for f in file:
        if f.endswith(".mp4"):
            f = f.replace(".mp4", "")
            files.append(f)
        elif f.endswith(".txt"):
            f = f.replace(".txt", "")
            transcripts.append(f)
    break

for file in files:
    try:
        # creating a folder named data
        if not os.path.exists("files_" + file):
            os.makedirs("files_" + file)
        else:
            send2trash.send2trash("files_" + file)
            os.makedirs("files_" + file)
        # if not created then raise error
    except OSError:
        print("Error: Creating directory of data")
    counted_sing = dict()
    counted_sing_ocr = dict()
    counted_plu = dict()
    counted_plu_ocr = dict()
    f = open('error.txt','w')
    f2 = open("outputs.txt","w")
    f2.close()
    try:
        if file not in transcripts:
            runFull(file, counted_sing, counted_sing_ocr, counted_plu, counted_plu_ocr)
        else:
            runWithTranscript(
                file, counted_sing, counted_sing_ocr, counted_plu, counted_plu_ocr
            )
    except Exception as e:
        f.write(file + "\n")
        f.write(str(e) + "\n")
        f.write("\n\n")
