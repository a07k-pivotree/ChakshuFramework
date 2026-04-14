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

## Docker Quick Concept

- Docker image: a packaged snapshot of your test environment.
- Docker container: a running instance created from that image.
- `docker exec ...` works only when a container is already running.

## Run With Docker

### Prerequisite

- Confirm a container is running before using `docker exec`:

```bash
docker ps
```

### User Setup

```bash
# Step 1 - clone your repo
git clone https://github.com/a07k-pivotree/ChakshuFramework.git
cd ChakshuFramework

# Step 2 - build image
docker build -t chakshu-qa .
```

### Option A: One-shot test run

```bash
docker run --rm -v "${PWD}/reports:/app/reports" chakshu-qa
```

### Option B: Keep container running, then run tests with docker exec

```bash
#open the docker desktop first
# Start long-running container
docker run -d --name chakshu-qa-dev -v "${PWD}:/app" chakshu-qa tail -f /dev/null

# Run specific tests inside the running container
docker exec -it chakshu-qa-dev pytest tests/test_checkout.py
docker exec -it chakshu-qa-dev pytest tests/test_login.py -q
docker exec -it chakshu-qa-dev pytest tests/ -q
```

To stop or remove the dev container:

```bash
docker stop chakshu-qa-dev
docker rm chakshu-qa-dev
```

To start the existing container:

```bash
docker start chakshu-qa-dev
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

## Docker vs Local Usage

- Docker-only users can keep running tests in Docker without reinstalling dependencies each time.
- Host commands like `pytest tests\test_checkout.py --headed` and `allure open ...` require local setup (venv + requirements + Allure CLI).
- In Docker, use Linux-style paths in pytest commands (`tests/test_checkout.py`).
- Headed mode in Docker usually needs extra GUI/X11 configuration.
