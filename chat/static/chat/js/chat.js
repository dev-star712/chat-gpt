const split_path = window.location.pathname.split('/')
const room_name = split_path[split_path.length - 1 ]
const chatSection = document.getElementById("chat-content")
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + room_name +'/'
)
const chat_div = document.querySelector(".chat")
const menu = document.querySelector(".menu")
const btnMenu = document.getElementById("btn-menu")
const notif_socket = new WebSocket(
    'ws://' + window.location.host + '/ws/notif/'
)

const room_api_url = '/api/chat/room/data/' + room_name

async function get_chats() {
    var response = await fetch(room_api_url)
    return response.json()
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
    chat_data.then((r)=>{
        for(var i in r) {
            create_chat_box(r[i].text, r[i].from_user)
        }
    })
}
function create_chat_box(message, sender) {
    if(sender == current_user) {
        var element = `
        <div class="message" id="me">
            <div>
                <h4>${sender}</h4>
                <p>${message}</p>
            </div>
        </div>
        `
    }else{ 
        var element = `
        <div class="message">
            <div>
                <h4>${sender}</h4>
                <p>${message}</p>
            </div>
        </div>`
    }
    chatSection.innerHTML += element
    scroll_bottom()

}

function scroll_bottom() {
    window.scrollTo(0, chat_div.scrollHeight)
}

function send_message() {
    var message = document.getElementById("message")
    chatSocket.send(JSON.stringify({"message":message.value}))
    message.value = ''
}
chatSocket.onerror = function(e) {
    console.log(e);
}
chatSocket.onmessage = function(m) {
    var json_parser = JSON.parse(m.data)
    create_chat_box(json_parser.message, json_parser.sender)
}
function openMenu() {
    menu.classList.toggle("active")
    if(menu.classList.contains("active")) {
      btnMenu.setAttribute("class", "fa fa-times")    
    } else {
      btnMenu.setAttribute("class", "fa fa-bars")    
    }
  }