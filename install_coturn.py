#!/usr/bin/env python3

import os
import subprocess
import shutil
import secrets
import socket

CONFIG_FILE = "/etc/turnserver.conf"
DEFAULT_FILE = "/etc/default/coturn"

REALM = "securecomm.local"
SECRET = secrets.token_hex(32)

def run(cmd):
    print(f"\n>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def main():
    if os.geteuid() != 0:
        raise SystemExit("Run this script as root (sudo).")

    print("Installing Coturn...")
    run(["apt", "update"])
    run(["apt", "install", "-y", "coturn"])

    if os.path.exists(CONFIG_FILE):
        shutil.copy(CONFIG_FILE, CONFIG_FILE + ".bak")

    ip = local_ip()

    config = f"""
listening-port=3478
tls-listening-port=5349

listening-ip={ip}
relay-ip={ip}

fingerprint

use-auth-secret
static-auth-secret={SECRET}

realm={REALM}

total-quota=100

bps-capacity=0

stale-nonce

no-loopback-peers
no-multicast-peers

simple-log
log-file=/var/log/turn.log

min-port=49152
max-port=49200

verbose
"""

    with open(CONFIG_FILE, "w") as f:
        f.write(config)

    with open(DEFAULT_FILE, "w") as f:
        f.write("TURNSERVER_ENABLED=1\n")

    run(["systemctl", "enable", "coturn"])
    run(["systemctl", "restart", "coturn"])

    print("\n====================================")
    print("Coturn installed successfully.")
    print(f"Listening IP : {ip}")
    print("TURN Port    : 3478")
    print("TLS Port     : 5349")
    print(f"Realm        : {REALM}")
    print(f"Secret       : {SECRET}")
    print("====================================")

if __name__ == "__main__":
    main()
