@echo off
pushd %~dp0

::Check python version
python --version
if %errorlevel% neq 0 (
    echo Python is not installed please install from: 
    echo     https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
    echo.
    echo Make sure check options:
    echo     pip, tcl/tk and python test suite features
    echo Also, make sure to "Add python to environment variables"
    echo.
    echo then run this script again
    pause
    start https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
    pause
    exit /b 1
)

:: Make sure the python virtual environment is setup
if not exist "environment" (
    python -m venv environment
)

:: Check if the virtual environment is activated
if /I "%VIRTUAL_ENV%" neq "%cd%\environment" (
    echo Activating virtual environment
    call environment\Scripts\activate.bat
)

:: Install python packages
pip install -r requirements.txt

popd