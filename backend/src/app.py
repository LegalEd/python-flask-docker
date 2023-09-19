import csv
import random
from flask import current_app
import json
from jsonschema import validate

from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@app.route("/")
def index():
    return render_template("index.html")


@sock.route("/echo")
def echo(sock):
    while True:
        data = sock.receive()
        sock.send(data)
        sock.send("backend")


# AP - convert Dockerfile to docker-compose.yml


# spot the XSS <image src=1 href=1 onerror="javascript:alert('This is an XSS vulnerability')"></image>
# <p><script>alert('This is an XSS vulnerability');</script></p>
# Const name = "<img src='x' onerror='alert(1)'>";
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
            current_app.logger.info(f"received messages are: {received_messages}")
            json_data = json.loads(data)
            # raise error if invalid
            # validate(instance=json_data, schema=json_schema)
            # valid_json = json.dumps(json_data, separators=(",", ":"))
            valid_json = json_data
            current_app.logger.info(f"received {valid_json}")
            if valid_json["kind"] == 1:  # saving messages
                received_messages.append(valid_json)
                current_app.logger.info(f"Saving: {valid_json}")
                # sock.send({"content": "Saving message"})
                # sock.close()

            elif valid_json["kind"] == 2:  # sending messages
                for message in received_messages:
                    messagehash = message["id"] + valid_json["pubkey"]
                    current_app.logger.info(f"message hash is : {messagehash}")
                    if message["pubkey"] == valid_json["pubkey"]:
                        # sock.send("no new messages")
                        continue
                    elif messagehash not in sent_messages:
                        sent_messages.append(messagehash)
                        current_app.logger.info(f"Sent: {message}")
                        sock.send(json.dumps(message))
                # sock.close()

            else:
                # sock.send({"content": "Saving message"})
                # sock.close()
                continue

        except Exception as e:
            sock.send({"content": f"error {e}"})
            current_app.logger.info(f"error: {e}")
            # sock.close()



@app.route("/random_joke")
def random_joke():

    with open("/app/src/jokes.csv", "r") as file:
        reader = csv.reader(file)
        jokes = list(reader)
        random_joke = random.choice(jokes)[0]
    return random_joke


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
