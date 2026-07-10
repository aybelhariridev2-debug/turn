# Dockerfile

FROM coturn/coturn:latest

# Copy Coturn configuration
COPY turnserver.conf /etc/coturn/turnserver.conf

# Start Coturn
ENTRYPOINT ["turnserver", "-c", "/etc/coturn/turnserver.conf", "-o"]
