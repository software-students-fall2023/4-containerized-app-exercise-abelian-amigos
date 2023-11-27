FROM python:3.11-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8002

CMD ["python3", "-m", "src.main"]