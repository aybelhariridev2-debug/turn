from flask import Flask
from flask_sock import Sock
import os

app = Flask(__name__)
sock = Sock(app)

clients = {}

@app.route("/")
def home():
    return {
        "name": "SecureComm Signaling Server",
        "status": "running"
    }

@sock.route("/ws")
def websocket(ws):

    client_id = None

    while True:
        data = ws.receive()

        if data is None:
            break

        if client_id is None:
            client_id = data
            clients[client_id] = ws
            print("Connected:", client_id)
            continue

        if ":" in data:

            target, message = data.split(":",1)

            if target in clients:
                try:
                    clients[target].send(message)
                except:
                    pass

    if client_id in clients:
        del clients[client_id]

if __name__ == "__main__":

    port = int(os.environ.get("PORT",8080))

    app.run(
        host="0.0.0.0",
        port=port
    )
