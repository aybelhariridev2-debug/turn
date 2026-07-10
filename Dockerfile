FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y \
    python3 \
    coturn && \
    apt clean

WORKDIR /app

COPY . .

CMD ["python3", "start.py"]
