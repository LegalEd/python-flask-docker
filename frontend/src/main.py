import csv
import random
from flask import current_app
from flask_sock import Sock
import json
from jsonschema import validate

import os

from flask import Flask, render_template_string, render_template
from flask_security import (
    Security,
    current_user,
    auth_required,
    hash_password,
    SQLAlchemySessionUserDatastore,
    permissions_accepted,
)
from database import db_session, init_db
from models import User, Role

# https://flask-security-too.readthedocs.io/en/stable/quickstart.html

# Create app
app = Flask(__name__)
sock = Sock(app)
app.config["DEBUG"] = True

# Generate a nice key using secrets.token_urlsafe()
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
)
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
    "SECURITY_PASSWORD_SALT", "146585145368132386173505678016728509634"
)
# Don't worry if email has findable domain
app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}

# manage sessions per request - make sure connections are closed and returned
app.teardown_appcontext(lambda exc: db_session.close())

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)


# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string("Hello {{current_user.email}}!")


@app.route("/user")
@auth_required()
@permissions_accepted("user-read")
def user_home():
    return render_template_string("Hello {{ current_user.email }} you are a user!")


# one time setup
with app.app_context():
    init_db()
    # Create a user and role to test with
    app.security.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )
    db_session.commit()
    if not app.security.datastore.find_user(email="test@me.com"):
        app.security.datastore.create_user(
            email="test@me.com", password=hash_password("password"), roles=["user"]
        )
    db_session.commit()


@app.route("/profile")
@auth_required()
def profile():
    return render_template("profile.html")


@app.route("/")
@auth_required()
def index():
    return render_template("index.html")


# # spot the XSS <image src=1 href=1 onerror="javascript:alert('This is an XSS vulnerability')"></image>
# # <p><script>alert('This is an XSS vulnerability');</script></p>
# # Const name = "<img src='x' onerror='alert(1)'>";
# # https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML
# # https://security.stackexchange.com/questions/127711/under-which-conditions-wouldnt-a-script-tag-run

# # {
# #   "id": <32-bytes lowercase hex-encoded sha256 of the serialized event data>,
# # a2 ea 4c 87 e8 3e ab 70 ed c4 f3 9c 2e 70 77 38 9c 3d d0 10 c2 0c ad fb 9c 58 d7 27 8c c3 de ec
# #   "pubkey": <32-bytes lowercase hex-encoded public key of the event creator>,
# #   "created_at": <unix timestamp in seconds>,
# #   "kind": <integer>,
# #   "tags": [
# #     ["e", <32-bytes hex of the id of another event>, <recommended relay URL>],
# #     ["p", <32-bytes hex of a pubkey>, <recommended relay URL>],
# #     ... // other kinds of tags may be included later
# #   ],
# #   "content": <arbitrary string>,
# #   "sig": <64-bytes hex of the signature of the sha256 hash of the serialized event data, which is the same as the "id" field>
# # }

# json_schema = {
#     "id": "notsr1",
#     "type": "object",
#     "properties": {
#         "id": {"type": "string", "minLength": 64, "maxLength": 64},
#         "username": {"type": "string", "minLength": 1, "maxLength": 64},
#         "pubkey": {"type": "string", "minLength": 64, "maxLength": 64},
#         "created_at": {"type": "number", "minimum": 1000000000, "exclusiveMaximum": 9999999999},
#         "kind": {"type": "number", "exclusiveMaximum": 4},
#         "tags": {"type": "array"},
#         "content": {"type": "string", "maxLength": 256},
#         "sig": {"type": "string", "minLength": 95, "maxLength": 95},
#     },
#     "required": ["id", "pubkey", "created_at", "kind"]
# }

received_messages = []
sent_messages = []


@sock.route("/nostr")
@auth_required()
def nostr(sock):
    while True:
        data = sock.receive()
        try:
            json_data = json.loads(data)
            # raise error if invalid
            validate(instance=json_data, schema=json_schema)
            # valid_json = json.dumps(json_data, separators=(",", ":"))
            valid_json = json_data
            current_app.logger.info(f"received {valid_json}")
            if valid_json["kind"] == 1:  # saving messages
                received_messages.append(valid_json)
                current_app.logger.info(f"Saving: {valid_json}")
                sock.send("Saving message")
                sock.close()

            elif valid_json["kind"] == 2:  # sending messages
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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route("/logout")
@auth_required()
def logout():
    return "logout"


@app.route("/random_joke")
@auth_required()
def random_joke():
    with open("/app/src/jokes.csv", "r") as file:
        reader = csv.reader(file)
        jokes = list(reader)
        random_joke = random.choice(jokes)[0]
    return random_joke


# app.config.from_pyfile('settings.py')

# import db.database as db
# db.init_app(app)
