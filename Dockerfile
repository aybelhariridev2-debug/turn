FROM coturn/coturn:latest

RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get clean

WORKDIR /app

COPY turnserver.conf /etc/coturn/turnserver.conf
COPY health.py /app/health.py
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

ENTRYPOINT ["/app/start.sh"]
