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


# {
#   "id": <32-bytes lowercase hex-encoded sha256 of the serialized event data>,
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
        "kind": {"type": "array",   "items": {"type": "number"}},
        "tags": {"type": "array"},
        "content": {"type": "string", "maxLength": 256},
        "sig": {"type": "string", "minLength": 64, "maxLength": 64},
    },
    "required": ["id", "pubkey", "created_at", "kind"]
}


@sock.route("/nostr")
def nostr(sock):
    while True:
        data = sock.receive()
        try:
            json_data = json.loads(data)
            # raise error if invalid
            validate(instance=json_data, schema=json_schema)
            sock.send(json_data)

        except Exception as e:
            sock.send(f"error {e}")
            current_app.logger.info(f"error: {e}")


@app.route("/random_joke")
def random_joke():

    with open("/app/src/jokes.csv", "r") as file:
        reader = csv.reader(file)
        jokes = list(reader)
        random_joke = random.choice(jokes)[0]
    return random_joke


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
