const room = document.getElementById("room")
const go_btn = document.getElementById("go")

const websocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notif/' 
)

go_btn.onclick = function() {
    window.location.href = "/room/" + room.value + '/' 
    
}
websocket.onmessage = function(e) {
    console.log(e)
}