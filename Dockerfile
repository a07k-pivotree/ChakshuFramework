FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright pytest pytest-html
RUN playwright install --with-deps chromium

COPY . .

CMD ["pytest", "tests/", "--html=reports/pytest-report.html", "--self-contained-html", "-v"]