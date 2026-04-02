@echo off
setlocal EnableExtensions

pushd "%~dp0"

for /f %%I in ('powershell -NoProfile -Command "(Get-Date).ToString(\"yyyy-MM-dd_HH-mm-ss\")"') do set "RUN_TIMESTAMP=%%I"

set "RUN_ROOT=reports\history\%RUN_TIMESTAMP%"
set "RESULTS_DIR=%RUN_ROOT%\allure-results"
set "REPORT_DIR=%RUN_ROOT%\allure-report"
set "PYTEST_EXIT=0"

if not exist "%RUN_ROOT%" mkdir "%RUN_ROOT%"

echo Running tests...
pytest tests\ --alluredir="%RESULTS_DIR%" %*
set "PYTEST_EXIT=%ERRORLEVEL%"

if not exist "%RESULTS_DIR%" (
    echo.
    echo No Allure results were created. Skipping report generation.
    popd
    exit /b %PYTEST_EXIT%
)

echo.
echo Generating Allure report...
allure generate "%RESULTS_DIR%" -o "%REPORT_DIR%" --clean
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
