const room = document.getElementById("room")
const go_btn = document.getElementById("go")



const websocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notif/' 
)
async function getMe() {
    var response = await fetch('/api/user/getMe')
    return response.json()
}

websocket.onopen = function() {
    var response = getMe()
    response.then((r) =>{

        websocket.send(JSON.stringify(r))
    })
}

function create_room_card(room_name, room_code) {

    var div_sm = document.createElement("div")
    div_sm.className = "col-sm-4 mb-2"

    var card = document.createElement("div")
    card.className = "card"

    var card_body = document.createElement("div")
    card_body.className = "card-body"

    var card_title = document.createElement("h5")
    card_title.className = "card-title"
    card_title.innerHTML = room_name

    var room_link = document.createElement("a")
    room_link.className = "btn btn-dark"
    room_link.href = '/chat/room/' + room_code
    room_link.innerHTML = "Join"

    card_body.appendChild(card_title)
    card_body.appendChild(room_link)
    card.appendChild(card_body)
    div_sm.appendChild(card)

    document.getElementById("card-row").appendChild(div_sm)

}


async function check_room(room_code){
    var response = await fetch(
        '/api/chat/room/data/' + room_code + '/'
    )
    return response.status
}

async function get_room(custom_url=false) {
    if (custom_url) {
        url = custom_url
    }else{
        url = '/api/chat/room/data'
    }
    var response = await fetch(url)
    return response.json()
}

function show_next_rooms() {
    var next_button = document.getElementById("next-button")
    var url_value = next_button.value
    var room_response = get_room(custom_url=url_value)
    show_room(room_response)
    next_button.remove()


}

function show_next_button(next_url){
    
    var button = document.createElement("button")
    button.className = "btn btn-outline-dark"
    button.value = next_url
    button.id = "next-button"
    button.innerHTML = "Next"
    button.setAttribute("onclick", "show_next_rooms()")
    document.getElementById("button-position").appendChild(button)

}



function show_room(request) { 

    request.then((r) =>{
        if(r.next) {
            show_next_button(r.next)
            console.log(r.next)
        }
        if(r.results && r.results.length != 0) {
            for(var i in r.results) {
                var room_name = r.results[i].room_name
                var room_code = r.results[i].room_code 
                create_room_card(room_name, room_code)
            }
        }
          
    })
}

if(go_btn) {
    var response_get_room = get_room(false)
    show_room(response_get_room)
    
    go_btn.onclick = function() {
        clean_message()
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
    var room_status = document.getElementById("room_status")
    data.is_public = room_status.value
    var response = post_data('/api/chat/room/data/', data=data)
    response.then((r) => {
        if(r.status && r.room_code) {
            create_response('Success, your room code is ' + r.room_code)
            create_response("Quick Join <a href='/chat/room/" + r.room_code + "' target='_blank'>Touch me")
        }
    })
    document.getElementById("room_code").value = ""

}

websocket.onmessage = function(e) {
    var data_json = JSON.parse(e.data)
    if(data_json.total_visitor) {
        var visitor_id = document.getElementById("total_visitor")
        visitor_id.innerHTML = data_json.total_visitor
    }

}