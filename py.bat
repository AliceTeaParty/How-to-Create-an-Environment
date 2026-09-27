@echo off
setlocal

set "PYTHON_TO_USE=F:\WPy64-313150\python\python.exe"

if not "%~1"=="" if exist "%~1" (
    for %%F in ("%~1") do if %%~zF EQU 0 (
        start "" code.exe "%%~fF"
        exit /b 0
    )
)

:execute
(
echo --------------------------------------------------------------------------------
echo Working Directory: "%CD%"
echo Executing: "%PYTHON_TO_USE%" %*
echo --------------------------------------------------------------------------------
) 1>&2
"%PYTHON_TO_USE%" %*
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" timeout /T 10
exit /b %EXIT_CODE%
