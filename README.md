# ChakshuFramework

An automation framework built with Playwright, pytest, and Page Object Model structure.

## Features

- Page Object Model (POM) design for maintainable test code
- Pytest-based execution with parameterization support
- Excel-driven test data via `openpyxl`
- Logging to `logs/framework.log`
- Screenshots captured in `screenshots/`
- Test artifacts and reports stored under `reports/`

## Installation

```bash
git clone ChakshuFramework
cd ChakshuFramework
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run Tests

```bash
pytest tests/test_login.py --headed
```

To generate fresh Allure results during the test run:

```bash
pytest tests/test_login.py --headed --alluredir=reports/allure-results --clean-alluredir
```

## Generate Allure Report

Use the helper script:

```powershell
.\generate-allure-report.ps1
```

This project uses Allure CLI `3.x`. In Allure 3, `allure generate` no longer supports `--clean`, so the script removes `reports/allure-report` before running:

```powershell
allure generate reports/allure-results -o reports/allure-report
```
After generating the report, it does get saved until again this above script is run and get replaced by the new report.
To Open the report, use the command:

```powershell
allure open reports/allure-report
```
It will open the report on the local server.