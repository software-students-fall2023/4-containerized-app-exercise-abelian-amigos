FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8001

CMD ["python3", "-m", "src.app"]
