import os
import subprocess

print("Starting Coturn...")

cmd = [
    "turnserver",
    "-c",
    "/app/turnserver.conf",
    "--log-file",
    "stdout",
]

subprocess.run(cmd)
