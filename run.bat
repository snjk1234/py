@echo off
chdir /d "%~dp0"

REM Check if Python embedded exists
if not exist "python\python.exe" (
    echo Python Embedded not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Run the Streamlit app
echo Starting Supervisor Commission System...
python\python.exe -m streamlit run main.py

pause
