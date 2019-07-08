@ECHO off
SET /A file_name_int = 0
setlocal enableextensions enabledelayedexpansion
cls

CALL :Demo1
CALL :Shutdown
EXIT /B 0

REM Demo1
:Demo1

git init
mkdir temp_files

CALL :MakeCommit
git checkout -b master-cached
git checkout master
CALL :MakeCommit

CALL :ShowChainsAndMessage "git checkout -b amazing-feature"
git checkout -b amazing-feature
CALL :MakeCommit
CALL :ShowChainsAndMessage "git commit -m 'Added new class'"
CALL :MakeCommit
CALL :ShowChainsAndMessage "git commit -m 'Added test'"
CALL :MakeCommit
CALL :ShowChainsAndMessage "git checkout -b refactor-for-feature"

REM Add random commit to master
git checkout master
CALL :MakeCommit
git checkout amazing-feature

git checkout -b refactor-for-feature
CALL :MakeCommit
CALL :ShowChainsAndMessage "git commit -m 'Did some refactoring on my awesome feature'"
CALL :MakeCommit

REM Add random commit to master
git checkout master
CALL :MakeCommit
git checkout refactor-for-feature

CALL :ShowChainsAndMessage "git commit -m 'Refactor some more'"
CALL :MakeCommit
git checkout amazing-feature
CALL :ShowChainsAndMessage "git commit -m 'Address review feedback for amazing-feature'"
CALL :MakeCommit

REM MERGE VERSION
CALL :ShowChainsAndMessage "git chains --merge --show amazing-feature refactor-for-feature"
cls
python ..\git-chains.py %* -m -s amazing-feature refactor-for-feature
timeout /t 4 >nul
CALL :ShowChainsAndMessage "git checkout refactor-for-feature"
CALL :ShowChainsAndMessage "git merge amazing-feature"
git checkout refactor-for-feature
git merge amazing-feature
CALL :ShowChainsAndMessage "The feature branch is now in the refactor chain to represent it is fully merged in."
git checkout amazing-feature
CALL :ShowChainsAndMessage "git commit -m 'Even more review feedback for amazing-feature'"
CALL :MakeCommit
CALL :ShowChainsAndMessage "Now the feature branch is not fully merged in to the refactor branch."
timeout /t 4 >nul
CALL :ShowChainsAndMessage "Fin"
timeout /t 4 >nul

REM REBASE VERSION
REM CALL :ShowChainsAndMessage "git chains --rebase --show amazing-feature refactor-for-feature"
REM cls
REM python ..\git-chains.py %* -r -s amazing-feature refactor-for-feature
REM timeout /t 4 >nul
REM CALL :ShowChainsAndMessage "git rebase amazing-feature refactor-for-feature"
REM git rebase amazing-feature refactor-for-feature
REM CALL :ShowChainsAndMessage "The rebase fixed our chain. Now our refactor PR can be targeted to our feature PR."
REM timeout /t 4 >nul
REM CALL :ShowChainsAndMessage "Fin"
REM timeout /t 4 >nul

EXIT /B 0

REM Begin methods

:ShowChainsAndMessage
cls
CALL :Chains
set num=0
set "line=%~1"
call :SlowType
timeout /t 2 >nul
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
ECHO.
ECHO.
REM set /p DUMMY=Hit ENTER to continue...
EXIT /B 0

:SlowType
set "letter=!line:~%num%,1!"
set "delay=%random%%random%%random%%random%%random%%random%%random%"
set "delay=%delay:~-6%"
if not "%letter%"=="" set /p "=%letter%" <nul
if "%letter%"==" " type IMASPACE.txt

:: adjust the speed higher is faster
set speed=7

::@ECHO off
for /L %%b in (1,%speed%,%delay%) do rem
::@ECHO on
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