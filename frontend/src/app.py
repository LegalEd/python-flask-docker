import csv
import sqlite3
import random
from flask import current_app
import json
from jsonschema import validate

from flask import Flask, render_template, request
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

from . import db


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/")
def index():
    return render_template("index.html")


# AP - convert Dockerfile to docker-compose.yml


# spot the XSS <image src=1 href=1 onerror="javascript:alert("This is an XSS vulnerability")"></image>
# <p><script>alert("This is an XSS vulnerability");</script></p>
# Const name = "<img src="x" onerror="alert(1)">";
# https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML
# https://security.stackexchange.com/questions/127711/under-which-conditions-wouldnt-a-script-tag-run

# {
#   "id": <32-bytes lowercase hex-encoded sha256 of the serialized event data>,
# a2 ea 4c 87 e8 3e ab 70 ed c4 f3 9c 2e 70 77 38 9c 3d d0 10 c2 0c ad fb 9c 58 d7 27 8c c3 de ec
#   "pubkey": <32-bytes lowercase hex-encoded public key of the event creator>,
#   "created_at": <unix timestamp in seconds>,
#   "kind": <integer>,
#   "tags": [
#     ["e", <32-bytes hex of the id of another event>, <recommended relay URL>],
#     ["p", <32-bytes hex of a pubkey>, <recommended relay URL>],
#     ... // other kinds of tags may be included later
#   ],
#   "content": <arbitrary string>,
#   "sig": <64-bytes hex of the signature of the sha256 hash of the serialized event data, which is the same as the "id" field>
# }

json_schema = {
    "id": "notsr1",
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 64, "maxLength": 64},
        "username": {"type": "string", "minLength": 1, "maxLength": 64},
        "pubkey": {"type": "string", "minLength": 64, "maxLength": 64},
        "created_at": {"type": "number", "minimum": 1000000000, "exclusiveMaximum": 9999999999},
        "kind": {"type": "number", "exclusiveMaximum": 4},
        "tags": {"type": "array"},
        "content": {"type": "string", "maxLength": 256},
        "sig": {"type": "string", "minLength": 95, "maxLength": 95},
    },
    "required": ["id", "pubkey", "created_at", "kind"]
}

received_messages = []
sent_messages = []

@sock.route("/nostr")
def nostr(sock):
    while True:
        data = sock.receive()
        try:
            json_data = json.loads(data)
            validate(instance=json_data, schema=json_schema)
            valid_json = json_data
            current_app.logger.info(f"received {valid_json}")



            # Saving messages:
            if valid_json["kind"] == 1:
                received_messages.append(valid_json)
                current_app.logger.info(f"Saving: {valid_json}")
                sock.send("Saving message")
                sock.close()

            # Sending messages:
            elif valid_json["kind"] == 2:
                for message in received_messages:
                    messagehash = message["id"] + valid_json["pubkey"]
                    current_app.logger.info(f"message hash is : {messagehash}")
                    if message["pubkey"] == valid_json["pubkey"]:
                        continue
                    elif messagehash not in sent_messages:
                        sent_messages.append(messagehash)
                        current_app.logger.info(f"Sent: {message}")
                        sock.send(message)
                sock.close()

            else:
                sock.send("Please specify kind")
                sock.close()

        except Exception as e:
            sock.send(f"error {e}")
            current_app.logger.info(f"error: {e}")
            sock.close()

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/logout")
def logout():
    return "logout"


# Ensure messages table exists:
with sqlite3.connect("messages_database.db") as messages_db_connection:
    messages_db_cursor = messages_db_connection.cursor()
    messages_db_cursor.execute("""CREATE TABLE IF NOT EXISTS messages_table (message_id TEXT PRIMARY KEY, username TEXT, timestamp TEXT, message TEXT)""")


@app.route("/save_message", methods=["POST"])
def save_message():
    """Save timestamp, username and message to messages db."""
    try:
        with sqlite3.connect("messages_database.db") as messages_db_connection:
            messages_db_cursor = messages_db_connection.cursor()

            data = request.get_json()
            content = data.get("content")
            timestamp = content.split(")")[0].split("(")[1].strip()
            username = content.split(")")[1].split(":")[0].strip()
            message = content.split(")")[1].split(":")[1].strip()
            message_id = (username + "_"+ timestamp).replace(" ", "_").replace("-", "_").replace(":", "_").lower()

            messages_db_cursor.execute("""INSERT INTO messages_table (message_id, username, timestamp, message) VALUES (?, ?, ?, ?)""", (message_id, username, timestamp, message))
            messages_db_connection.commit()
        return {"message": "Message saved successfully"}, 200
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
