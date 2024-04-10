@echo off


taskkill /IM pythonw.exe /F
call "%cd%\.venv\Scripts\activate.bat"
start pythonw.exe "main.py"