@ECHO off
SET /A file_name_int = 0
cls

CALL :Demo1
CALL :Shutdown
EXIT /B 0

REM Demo1
:Demo1

git init
mkdir temp_files
CALL :Waiter

CALL :MakeCommit
CALL :MakeCommit

CALL :ShowChainsAndMessage "We have committed to master...boring, but we gotta start somewhere. Let's add 10 more commits."

CALL :MakeCommit
CALL :MakeCommit
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
CALL :ShowChainsAndMessage "Spectacular. We now have a refactor happening. Let's do some edits."

CALL :MakeCommit
CALL :MakeCommit
CALL :ShowChainsAndMessage "Beautiful. Amazing. We got some feedback on our feature, let's do some editing there."

git checkout Feature
CALL :MakeCommit
CALL :ShowChainsAndMessage "Oh noes, our refactor is now out of date! How do we resolve this?"

CALL :Chains F R
echo "Seems like a good suggestion, let's try it!"
CALL :Waiter
cls

git checkout Refactor
git merge Feature
CALL :ShowChainsAndMessage "We've now completed the checkout and merge."

EXIT /B 0

REM Begin methods

:ShowChainsAndMessage
CALL :Chains
set num=0
set "line=%~1"
call :SlowType
CALL :Waiter
EXIT /B 0

:MakeCommit
CALL :Generate_rando_file
git stage .
git commit -m "."
cls
EXIT /B 0

:Chains
python ..\git-chains.py %*
EXIT /B 0

:Generate_rando_file
ECHO "hello world" >> "temp_files\\%file_name_int%.txt"
SET /A file_name_int = %file_name_int% + 1
EXIT /B 0

:Waiter
set /p DUMMY=Hit ENTER to continue...
EXIT /B 0

:SlowType
set "letter=!line:~%num%,1!"
set "delay=%random%%random%%random%%random%%random%%random%%random%"
set "delay=%delay:~-6%"
if not "%letter%"=="" set /p "=a%bs%%letter%" <nul

:: adjust the speed higher is faster
set speed=7

for /L %%b in (1,%speed%,%delay%) do rem
if "%letter%"=="" echo.&EXIT /B 0
set /a num+=1
goto :SlowType

:Shutdown
cls
ECHO Cleaning up repositories...
rmdir /S /Q .git
rmdir /S /Q temp_files
ECHO Closing up shop.
EXIT /B 0