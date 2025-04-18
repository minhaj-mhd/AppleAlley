FROM python:3.11-slim

WORKDIR /app

COPY requirments.txt /app/

RUN pip install --no-cache-dir -r requirments.txt

COPY . /app/

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

