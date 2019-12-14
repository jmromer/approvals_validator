FROM python:3.8.0-slim

WORKDIR /app

COPY requirements.txt ./
COPY requirements.test.txt ./

RUN pip install -r requirements.test.txt

COPY . /app

CMD [ "./test"]
