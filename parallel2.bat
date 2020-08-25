@echo off
setlocal
set "lock=%temp%\wait%random%.lock"

:: Launch processes asynchronously, with stream 9 redirected to a lock file.
:: The lock file will remain locked until the script ends.
start "" 9>"%lock%1" python 4e.topic_find_ocr_kde.py
start "" 9>"%lock%2" python 4d.topic_find_kde.py

:Wait for both processes to finish (wait until lock files are no longer locked)
1>nul 2>nul ping /n 2 ::1
for %%N in (1 2) do (
  (call ) 9>"%lock%%%N" || goto :Wait
) 2>nul

::delete the lock files
del "%lock%*"

:: Finish up
echo Done - ready to continue ranking