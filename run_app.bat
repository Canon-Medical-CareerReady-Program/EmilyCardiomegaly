@echo off
pushd %~dp0
:: This is a windows batch script which will run all tests in the project

if not exist "environment" (
    call setup.bat
)

setlocal
    :: Check if the virtual environment is activated
    if /I "%VIRTUAL_ENV%" neq "%cd%\environment" (
        echo Activating virtual environment
        call environment\Scripts\activate.bat
    )

    call python Cardiomegaly\main.py
endlocal
popd