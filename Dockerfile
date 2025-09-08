FROM python:slim

COPY ./dist/bot-0.1.0-py3-none-any.whl ./dist/bot-0.1.0.tar.gz /dist/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir /dist/bot-0.1.0-py3-none-any.whl 
RUN tar xzvf /dist/bot-0.1.1.tar.gz

WORKDIR /bot-0.1.1/

RUN mkdir -p ./downloads/audio
RUN mkdir -p ./downloads/metadata
RUN mkdir -p ./logs


CMD ["python", "bot/main.py"]
