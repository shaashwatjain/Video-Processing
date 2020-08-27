@ECHO OFF
:: This batch file is for running the project from start to end
TITLE Video Tagging Research project
ECHO Please ensure that your video is in the project folder and is named video.mp4
ECHO Converting to audio
python 1.convert_to_audio.py
ECHO Converting to chunks (This might take some time for larger videos)
python 2b.decibles_try.py
python 3a.screenshots.py
::ECHO If you have a youtube transcript, place it in "files/" and name it "transcript_yt.txt" in specified format.
::ECHO If not... press enter
::PAUSE
ECHO Now we'll parallel compute the transcripts
call parallel.bat
:: start /wait cmd.exe /c "python 3a.screenshots.py & python 3b.ocr_gen.py"
:: python 3b.transcript(parallel).py
ECHO Transcripts generated. Let's find topics
call parallel2.bat
ECHO Ranking...
python 5.ranking.py
ECHO Subclipping
python 6.subclipping.py
PAUSE