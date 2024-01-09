function getCurrentFormattedDateTime() {
    // Get current date, and format as desired
    const currentDate = new Date();
    const seconds = String(currentDate.getSeconds()).padStart(2, "0");
    const minutes = String(currentDate.getMinutes()).padStart(2, "0");
    const hours = String(currentDate.getHours()).padStart(2, "0");
    const day = String(currentDate.getDate()).padStart(2, "0");
    const month = String(currentDate.getMonth() + 1).padStart(2, "0");
    const year = String(currentDate.getFullYear()).slice(-2);
    return `(${year}-${month}-${day} ${hours}:${minutes}:${seconds})`;
}


function saveMessage(valid_json) {
    // POST request to send message content:
    const data = { content: valid_json.content };
    fetch("/save_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                console.log("Message saved successfully");
            } else {
                console.error("Failed to save message");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

const log = (text, color) => {
    // Adding a sent message to the webpage HTML
    document.getElementById("log").innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};


const d = new Date();
let time = d.getTime();
time = JSON.stringify(time);


var data = {
    "id": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "pubkey": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "username": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "created_at": 1234567890,
    "kind": 1,
    "tags": [],
    "content": "This is the first message",
    "sig": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
};


const host = "localhost:8080";
const socket = new WebSocket("ws://" + host + "/nostr");

document.getElementById("form").onsubmit = ev => {
    ev.preventDefault();

    const textField = document.getElementById("text");
    const user = document.getElementById("messageID");
    const timestamp = getCurrentFormattedDateTime();

    // Check if username or text field is empty:
    if (!user.value.trim() || !textField.value.trim()) {
        console.log("Username and message cannot be empty.");
        return;
    }

    // Update the existing data object with new values:
    data.username = user.value;
    data.content = timestamp + " " + data.username + ": " + textField.value;
    const hash = CryptoJS.MD5(data.content).toString();
    data.pubkey = time;
    data.id = hash + hash;
    log(text = ">>> " + data.content, color = "#101088");

    // Send the message through the socket:
    socket.send(JSON.stringify(data));
    textField.value = "";
};


const socket2 = new WebSocket("ws://" + host + "/nostr");
socket2.addEventListener(
    // Receiving all current messages
    "message", ev => {
        var receivedMessage = JSON.parse(ev.data);
        saveMessage(receivedMessage);
        log(text = "<<< " + receivedMessage.content, color = "#ca0000");

        console.log(typeof ev);
        ev = "";
    }
);


setInterval(
    hander = function () {
        // get data
        var getData = {
            "id": "banbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanb",
            "pubkey": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "created_at": 1234567890,
            "kind": 2,
            "tags": [],
            "content": "",
            "sig": "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        };

        getData.pubkey = time;
        console.log(getData);
        payload = JSON.stringify(getData);
        console.log("polling website");
        console.log(payload)
        socket2.send(payload)
    },
    timeout = 10000 // Poll every 10000ms
);


