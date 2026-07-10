FROM coturn/coturn:latest
COPY turnserver.conf /etc/coturn/turnserver.conf
# host networking is the simplest correct way to expose all TURN + relay ports
ENTRYPOINT ["turnserver", "-c", "/etc/coturn/turnserver.conf", "-o", "--no-cli"]
