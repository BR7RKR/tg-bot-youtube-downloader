FROM python:3.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./bot /app/bot
COPY ./requirements.txt /app
COPY ./pytube /app/pytube
COPY bot/app.py /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]