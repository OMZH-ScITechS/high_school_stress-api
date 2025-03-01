FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY app.py /app/
COPY newmodel_f1.pkl /app/
COPY newmodel_f2.pkl /app/
COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

EXPOSE 5000

HEALTHCHECK CMD curl --fail http://localhost:5000/_stcore/health

ENTRYPOINT ["python", "app.py"]