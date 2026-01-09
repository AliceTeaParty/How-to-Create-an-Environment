@echo off
setlocal

set "PYTHON_TO_USE=D:\WPy64-312101\python\python.exe"

:execute
echo --- Using: %PYTHON_TO_USE% ---
echo --- Working Directory: %CD% ---
echo --- Executing: %* ---
"%PYTHON_TO_USE%" %*
