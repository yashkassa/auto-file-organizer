@echo off
echo Running Auto File Sorter...
python "%~dp0main.py" %*
if %errorlevel% neq 0 (
    echo Something went wrong. Please check your Python installation or the script.
)
pause
