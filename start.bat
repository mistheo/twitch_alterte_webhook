@echo off
setlocal

rem Activate the virtual environment
call ".venv\Scripts\activate.bat"

rem Check if an argument is provided
if "%1"=="" (
    rem If no argument is provided, execute the Python script without any arguments
    pythonw.exe "main.py"
) else (
    pythonw.exe "main.py" "%1"
)


timeout 5 > nul
