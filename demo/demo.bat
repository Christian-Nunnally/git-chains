@ECHO off
SET /A file_name_int = 0
cls

git init
mkdir temp_files
CALL :Waiter

CALL :MakeCommit
CALL :MakeCommit

CALL :ShowChainsAndMessage "We have committed to master...very boring, but we gotta start somewhere."

CALL :MakeCommit
CALL :MakeCommit
CALL :MakeCommit
CALL :MakeCommit
CALL :MakeCommit
CALL :MakeCommit
CALL :MakeCommit
CALL :MakeCommit
CALL :ShowChainsAndMessage "The bubbles to the left of 'master' indicate we have more than 10 commits ahead of our current state."

git checkout -b Feature
CALL :MakeCommit

CALL :ShowChainsAndMessage "We have now created a feature branch. Exciting, amaze. Lets add some commits."

CALL :MakeCommit
CALL :MakeCommit
CALL :ShowChainsAndMessage "We now have some commits to our feature. Time to start a refactor! Easy, let's branch off our feature."

git checkout -b Refactor

CALL :MakeCommit
CALL :ShowChainsAndMessage "Spectacular. We now have a refactor happening."

CALL :Shutdown
EXIT /B 0


REM Begin methods

:ShowChainsAndMessage
CALL :Chains
echo %~1
CALL :Waiter
EXIT /B 0

:MakeCommit
CALL :Generate_rando_file
git stage .
git commit -m "."
cls
EXIT /B 0

:Chains
python ..\git-chains.py
EXIT /B 0

:Generate_rando_file
ECHO "hello world" >> "temp_files\\%file_name_int%.txt"
SET /A file_name_int = %file_name_int% + 1
EXIT /B 0

:Waiter
set /p DUMMY=Hit ENTER to continue...
EXIT /B 0

:Shutdown
cls
ECHO Cleaning up repositories...
rmdir /S /Q .git
rmdir /S /Q temp_files
ECHO Closing up shop.
CALL :Waiter
EXIT /B 0