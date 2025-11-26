@echo off
echo ================================================
echo   Supervisor Commission System - Setup
echo ================================================
echo.

REM Create directories
if not exist "python" mkdir python
if not exist "downloads" mkdir downloads

REM Download Python Embedded
echo [1/3] Downloading Python Embedded...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-embed-amd64.zip' -OutFile 'downloads\python-embed.zip'}"

REM Extract Python
echo [2/3] Extracting Python...
powershell -Command "Expand-Archive -Path 'downloads\python-embed.zip' -DestinationPath 'python' -Force"

REM Enable pip
echo [3/3] Setting up pip...
cd python
echo import sys > sitecustomize.py
echo import os >> sitecustomize.py
echo site_packages = os.path.join(os.path.dirname(__file__), 'Lib', 'site-packages') >> sitecustomize.py
echo sys.path.insert(0, site_packages) >> sitecustomize.py

REM Uncomment the import site line in python311._pth
powershell -Command "(Get-Content 'python311._pth') -replace '#import', 'import' | Set-Content 'python311._pth'"

REM Download get-pip.py
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'"
python.exe get-pip.py

REM Install requirements
cd ..
python\Scripts\pip.exe install -r requirements.txt

echo.
echo ================================================
echo   Setup Complete!
echo   Run 'run.bat' to start the application
echo ================================================
pause
