// need to check host is up. Try and retry
// need to fix html injection


const log = (text, color) => {
    document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
};

const d = new Date();
let time = d.getTime();
time = JSON.stringify(time);



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
    data.content = textField.value;
    hash = CryptoJS.MD5(data.content).toString()
    data.pubkey = time;
    console.log(hash);

    data.id = hash + hash;




    log('>>> ' + data.id + ':' + data.content, 'red');
    
    // send data
    socket.send(JSON.stringify(data));
    textField.value = '';
    



};

const socket2 = new WebSocket('ws://' + host + '/nostr');
socket2.addEventListener('message', ev => {
var receivedMessage = JSON.parse(ev.data);
log('<<< ' + receivedMessage.id + ':' + receivedMessage.content, 'blue');

console.log(typeof ev);
ev = '';
});

setInterval(function(){

    // get data


    var getData = {
        "id": "banbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanbanb", 
        "pubkey": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 
        "created_at": 1234567890, 
        "kind": 2, 
        "tags": [], 
        "content": "", 
        "sig": "baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"};


    getData.pubkey = time;
    console.log(getData);
    payload = JSON.stringify(getData);
    console.log("polling website");
    console.log(payload)
    socket2.send(payload)
    



}, 10000); // Poll every 10000ms


