FROM ubuntu:20.04

ARG ENVIRONMENT_NAME
ENV ENVIRONMENT_NAME=${ENVIRONMENT_NAME:-'DEVELOPMENT'}
RUN echo Build in $ENVIRONMENT_NAME environment

RUN \
    apt-get update && \
    apt-get install -y \
      python3 \
      python3-pip \
      git

ADD . /app
WORKDIR /app

RUN pip install --no-cache-dir -e .

CMD steam-deals
