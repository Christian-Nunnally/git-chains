git init
@ECHO off
set /p DUMMY=Hit ENTER to continue...
@ECHO on

python ..\chains.py

@ECHO off
ECHO Cleaning up repositories...
rmdir /S /Q .git