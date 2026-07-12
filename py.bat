@echo off
setlocal

set "PYTHON_TO_USE=C:\WPy64-313-Vapoursynth R73\python\python.exe"

:execute
echo --------------------------------------------------------------------------------
echo Working Directory: "%CD%"
echo Executing: "%PYTHON_TO_USE%" %*
echo --------------------------------------------------------------------------------
"%PYTHON_TO_USE%" %*
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" pause
exit /b %EXIT_CODE%
