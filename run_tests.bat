@echo off
setlocal EnableExtensions

pushd "%~dp0"

set "TARGET=tests"
set "EXTRA_ARGS="

if not "%~1"=="" (
    set "FIRST_ARG=%~1"
    if /i not "%FIRST_ARG:~0,1%"=="-" (
        set "TARGET=%~1"
        shift
    )
)

:collect_args
if "%~1"=="" goto args_done
set "EXTRA_ARGS=%EXTRA_ARGS% %~1"
shift
goto collect_args

:args_done
for /f %%I in ('powershell -NoProfile -Command "(Get-Date).ToString(\"yyyy-MM-dd_HH-mm-ss\")"') do set "RUN_TIMESTAMP=%%I"

set "RUN_ROOT=reports\history\%RUN_TIMESTAMP%"
set "RESULTS_DIR=%RUN_ROOT%\allure-results"
set "REPORT_DIR=%RUN_ROOT%\allure-report"
set "PYTEST_EXIT=0"

if not exist "%RUN_ROOT%" mkdir "%RUN_ROOT%"

echo Running tests...
pytest "%TARGET%" --alluredir="%RESULTS_DIR%"%EXTRA_ARGS%
set "PYTEST_EXIT=%ERRORLEVEL%"

if not exist "%RESULTS_DIR%" (
    echo.
    echo No Allure results were created. Skipping report generation.
    popd
    exit /b %PYTEST_EXIT%
)

echo.
echo Generating Allure report...
allure generate "%RESULTS_DIR%" -o "%REPORT_DIR%"
if errorlevel 1 (
    set "ALLURE_EXIT=%ERRORLEVEL%"
    echo Allure report generation failed.
    popd
    exit /b %ALLURE_EXIT%
)

echo.
echo Results saved to: %RESULTS_DIR%
echo Report saved to: %REPORT_DIR%
echo Open report with: allure open "%REPORT_DIR%"

popd
exit /b %PYTEST_EXIT%
