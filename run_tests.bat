@echo off
pushd %~dp0
:: This is a windows batch script which will run all tests in the project

set METRICS_DIR=.metrics
IF EXIST %METRICS_DIR% DEL /F %METRICS_DIR%

if not exist "environment" (
    call setup.bat
)

setlocal
    :: Check if the virtual environment is activated
    if /I "%VIRTUAL_ENV%" neq "%cd%\environment" (
        echo Activating virtual environment
        call environment\Scripts\activate.bat
    )

    call python -m pytest -o log_cli=False --ignore=environment --cov=Cardiomegaly --cov-report xml:%METRICS_DIR%\coverage.xml --cov-report html:%METRICS_DIR%\html
    set TEST_RESULT_ERROR_LEVEL=%errorlevel%
    call pylint --output-format=parseable --reports=no --exit-zero cacs > %METRICS_DIR%\pylint.log
    exit /b %TEST_RESULT_ERROR_LEVEL%
endlocal
popd