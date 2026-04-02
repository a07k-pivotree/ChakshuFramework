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

To run a particular test file and automatically generate a timestamped Allure report:

```powershell
.\run_tests.bat tests\test_login.py --headed
```

This creates:

- Allure results in `reports\history\<timestamp>\allure-results`
- Allure report in `reports\history\<timestamp>\allure-report`

Example:

```powershell
.\run_tests.bat tests\test_login.py --headed
```

## Open The Latest Report

```powershell
allure open "reports\history\2026-04-02_17-42-40\allure-report"
```

If you want to check the latest timestamp first:

```powershell
Get-ChildItem reports\history -Directory | Sort-Object Name -Descending
```

## Generate A Report From Existing Results

If you already have results in `reports\allure-results` and want to generate a new standalone report from them:

```powershell
.\generate-allure-report.ps1
```

This saves the generated report under:

```text
reports\generated-reports\<timestamp>
```

## Open Older Reports

To open an older saved report:

```powershell
allure open "reports\history\<older-timestamp>\allure-report"
```

Example:

```powershell
allure open "reports\history\2026-04-02_17-18-56\allure-report"
```

## What Old Reports Are Available

List all saved historical runs:

```powershell
Get-ChildItem reports\history -Directory | Sort-Object Name -Descending
```

Current examples in this repo:

- `2026-04-02_17-42-40`
- `2026-04-02_17-18-56`
