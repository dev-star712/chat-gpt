const room = document.getElementById("room")
const go_btn = document.getElementById("go")

const websocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notif/' 
)

function check_room() {
    console.log("i clicked")
}

async function check_room(room_code){
    var response = await fetch(
        '/api/chat/room/data/' + room_code + '/'
    )
    return response.status
}
if(go_btn) {
    go_btn.onclick = function() {
        message_id.innerHTML = ""
        var room_code = document.getElementById("room_code")
        if(room_code.value.length == 0) {
            return 0
        }
        room_code.value = ''
        var response = check_room(room_code.value)
        response.then((r) => {
            if(r == 404) {
                create_response("Room Not found!", failed=true)
            }
            else if(r == 200) {
                create_response("yeah, you got it!")
            }
            else {
                create_response("Invalid response!", failed=true)
            }
        })
        
    }
}

function make_room(){
    var data = get_fields()
    var response = post_data('/api/chat/room/data/', data=data)
    response.then((r) => {
        if(r.status && r.room_code) {
            create_response('Success, your room code is ' + r.room_code)
        }
    })
}

websocket.onmessage = function(e) {
    console.log(e)
}