FROM python:3.10-bullseye

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y gcc

RUN pip install --upgrade pip

RUN pip install rasa-sdk==3.6.2 pymongo

CMD ["rasa", "run", "actions", "--port", "5055", "--debug"]
