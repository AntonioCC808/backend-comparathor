FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set PYTHONPATH so `app/` is recognized
ENV PYTHONPATH=/app

CMD ["python", "-m", "app.main"]

