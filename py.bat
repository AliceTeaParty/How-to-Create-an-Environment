@echo off
setlocal

set "PYTHON_TO_USE=C:\green\WPy64-313110\python\python.exe"

:execute
echo Working Directory: "%CD%"
echo Executing: "%PYTHON_TO_USE%" %*
"%PYTHON_TO_USE%" %*

PAUSE
