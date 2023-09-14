// need to check host is up. Try and retry
// need to fix html injection

const log = (text, color) => {
    document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};


var data = {"id": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 
            "pubkey": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "created_at": 1234567890,
            "kind": 1,
            "tags": [],
            "content": "This is the first message",
            "sig": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"};





const host = "localhost:8080" ; 
const socket = new WebSocket('ws://' + host + '/nostr');


document.getElementById('form').onsubmit = ev => {
    ev.preventDefault();
    const textField = document.getElementById('text');
    const messageID = document.getElementById('messageID');
    data.content = textField.value;
    data.id = messageID.value;
    data.pubkey = messageID.value;
    log('>>> ' + data.id + ':' + data.content, 'red');
    
    // send data
    socket.send(JSON.stringify(data));
    textField.value = '';
    



};

const socket2 = new WebSocket('ws://' + host + '/nostr');

setInterval(function(){

    // get data
    socket.addEventListener('message', ev => {
    console.log(ev);
    console.log(ev.data)
    var receivedMessage = JSON.parse(ev.data);
    log('<<< ' + receivedMessage.id + ':' + receivedMessage.content, 'blue');


    console.log(typeof ev);
});

    var getData = {"id": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 
            "pubkey": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "created_at": 1234567890,
            "kind": 2,
            "tags": [],
            "content": "",
            "sig": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"};
    getData.id = messageID.value;
    getData.pubkey = messageID.value;
    socket2.send(JSON.stringify(getData))
    console.log("polling website");

}, 1000); // Poll every 1000ms


