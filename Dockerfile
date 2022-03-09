FROM ubuntu:20.04

RUN \
    apt-get update && \
    apt-get install -y \
      python3 \
      python3-pip
ADD . /app
WORKDIR /app

RUN pip install .

CMD ["python3", "steam_deals/main.py", "--port", "5000"]
