const split_path = window.location.pathname.split('/')
const room_name = split_path[split_path.length - 1 ]

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + room_name +'/'
)

const notif_socket = new WebSocket(
    'ws://' + window.location.host + '/ws/notif/'
)

const chat_div = document.getElementById("chat")

const submit_btn = document.getElementById("submit")

const room_api_url = '/api/chat/room/data/' + room_name

async function get_chats() {
    var response = await fetch(room_api_url)
    return response.json()
}

function create_chat_box(message, sender='Anon') {
    var div_chat_box = document.createElement("div")
    div_chat_box.className = "chat-box"

    var author = document.createElement("h4")
    author.className = "author"
    author.innerHTML = sender

    var p = document.createElement("p")
    p.innerHTML= message

    div_chat_box.appendChild(author)
    div_chat_box.appendChild(p)

    chat_div.appendChild(div_chat_box)

    chat_div.scrollTop = chat_div.scrollHeight

}


notif_socket.onopen = function(n) {
    console.log('notif socked opened!')
    notif_socket.send(
        JSON.stringify(
            {
                "room":room_name,
                "joined":true
            }
        )
    )
}

chatSocket.onopen = function() {
    var chat_data = get_chats()
    chat_data.then(
        (response) => {
        if(response.length !== 0) {
            for(i of response) {
                author = i.from_user 
                message = i.text 
                create_chat_box(message, author)
                }
            }
        }
    )
}
chatSocket.onerror = function(e) {
    console.log(e);
}
chatSocket.onmessage = function(m) {
    var json_parser = JSON.parse(m.data)
    create_chat_box(json_parser['message'], json_parser['sender'])
}

submit_btn.onclick = function(e) {
    var msg = document.getElementById("msg")
    if(msg.value.length < 6) {
        msg.value = ''
        return false;
    }
    var data_json = JSON.stringify({
        "message":msg.value
    })
    chatSocket.send(data_json)
    msg.value = ''
}