FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download de_core_news_sm

COPY . .

CMD ["gunicorn", "spacy_api:app", "--bind", "0.0.0.0:10000"]
