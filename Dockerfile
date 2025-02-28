FROM python:latest
WORKDIR /app
COPY . /app
CMD ["python", "-m", "http.server", "80"]
