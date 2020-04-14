FROM python:3.7.3-slim

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENV PYTHONPATH=/app
CMD ["gunicorn", "-w", "10", "--threads", "10", "-b", "0.0.0.0:5050", "flight_paths.app:app"]
