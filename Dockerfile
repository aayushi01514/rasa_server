# FROM rasa/rasa:3.6.21-full

# WORKDIR /app

# COPY . /app

# EXPOSE 5005

# CMD rasa run --enable-api --cors "*" --debug --port ${PORT:-5005}

FROM rasa/rasa:3.6.21-full

USER root

RUN apt-get update && apt-get install -y gcc python3-dev libffi-dev libssl-dev

WORKDIR /app

COPY . .

# Example: install extras if needed
# RUN pip install spacy

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug", "--port", "${PORT:-5005}"]
