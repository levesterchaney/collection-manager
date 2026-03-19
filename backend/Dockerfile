FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev openssl-dev cargo jpeg-dev zlib-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "collection_manager.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
