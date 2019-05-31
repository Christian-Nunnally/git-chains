@ECHO off
SET /A file_name_int = 0
cls

git init
mkdir temp_files
CALL :Waiter

CALL :MakeCommit

CALL :Chains
echo We have committed to master...very boring, but we gotta start somewhere.
CALL :Waiter

CALL :MakeCommit

CALL :Chains
CALL :Waiter

CALL :Shutdown
EXIT /B 0


REM Begin methods

:Chains
python ..\chains.py
EXIT /B 0

:MakeCommit
CALL :Generate_rando_file
git stage .
git commit -m "."
cls
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