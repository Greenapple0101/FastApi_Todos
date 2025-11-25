FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# PythonPath 추가 (fastapi-app 내부 실행용)
ENV PYTHONPATH="/app"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]
