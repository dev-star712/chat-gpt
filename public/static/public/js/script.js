function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const room_row = document.getElementById("room-row")
const message_id = document.getElementById("message")
const header_token = getCookie('csrftoken')

const register_url = '/api/user/register'
const login_url = '/api/user/login'

async function post_data(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type':'application/json',
            'X-CsrfToken':header_token
        }
    })
    return response.json()
}
function create_response(text, failed=false) {
    var div = document.createElement("div")
    if(failed){
        div.className = "alert alert-danger"
        div.innerHTML = "<strong>Failed!</strong> " + text 
    }else{
        div.className = "alert alert-success"
        div.innerHTML = "<strong>Success!</strong> " + text 
    }
    

    message_id.appendChild(div)

}

function get_fields(){
    let data = {};
    var input = document.querySelectorAll('input')
    for(i in input) {
        if(input[i].name && input[i].value) {
            data[input[i].name] = input[i].value
        }
    }
    return data 
}

function login_user() {
    let data = get_fields()
    post_data(login_url, data).then((response) => {
        if(response.success) {
            create_response('Logged in! Redirecting...')
            window.location.pathname = '/chat/'
        }else{
            var response = response ? response.message : response.detail
            create_response(response, failed=true)
        }
    }
    )
    clean_message()

}
function clean_inputs() { 
    var data = document.querySelectorAll("input")
    for(i in data){
        if(data[i].type !== 'hidden') {
            data[i].value = ''
        }
    }
}

function register_user() {
    clean_message()
    let data = get_fields()
    post_data(register_url, data).then((response) => {
        if(response.success) { 
            create_response('Registered, you can login now')
            clean_inputs()
        }else{
            for(i in response) {
                var raw_response = response[i][0]
                if(raw_response == 'This field is required.') {
                    text = "Missing Form!"
                }else{
                    text = raw_response
                }

                create_response(text, failed=true)
            }
        }


        }

    )

}
function clean_message() {
    document.getElementById("message").innerHTML = ''
}
function change_password() {
    clean_message()
    var data = {}
    var input_fields = document.querySelectorAll("input")
    for(var i in input_fields) {
        if(input_fields[i].type == 'password' && input_fields[i].value.length != 0) {
            data[input_fields[i].name] = input_fields[i].value
        }
    }
    var response = post_data('/api/user/change-password', data=data)
    response.then((r) => {
        if(r.success) {
            create_response("Password Changed!", failed=false)
        }else{
            for(i in r) {
                create_response(r[i][0].message, failed=true)
            }
        }
    })
}
function update_user() {
    clean_message()
    var data = get_fields()
    var z = post_data('/api/user/profile', data)
    z.then((r) => {
        if(r.success) {
            create_response("Changed!")
        }else{
            if(r.length != 0) {
                for(var i in r) {
                    //console.log(r[i][0].message)
                    create_response(r[i][0].message, failed=true)
                }
            }
        }
    })
}
function create_my_room_card(room_name, room_code) {
    var element = `
    <div class="col-md-3 mt-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title mb-3">${room_name}
                            <i class="ml-2 fa fa-files-o" onclick="copy_room_url(this)" room_code="${room_code}"></i>
                        </h5>
                        <a href="/chat/room/${room_code}" class="btn btn-dark"><i class="fa fa-paper-plane-o fa-2x"></i></a>
                        <button class="btn btn-primary" room_code="${room_code}" onclick="refresh_code(this)"><i class="fa fa-refresh fa-2x"></i></button>
                        <button class="btn btn-danger" room_code="${room_code}" onclick="delete_room(this)"><i class="fa fa-trash-o fa-2x"></i></button>
                        
                    </div>
                </div>
    `
    room_row.innerHTML += element
}
function copy_room_url(element){
    var room_code = element.getAttribute("room_code")
    console.log(room_code)
    var room_url = `${window.location.host}/chat/room/${room_code}`
    //element.select.setSelectionRange(0, 9999)
    navigator.clipboard.writeText(room_url)
    alert("Copied!")
}
async function request_delete_room(room_code) {
    var response = await fetch('/api/user/delete-room/' + room_code)
    return response.json()
}

function delete_room(element) {
    var room_code = element.getAttribute("room_code")
    var response = request_delete_room(room_code)
    response.then((r) =>{
        if(r.success) {
            create_response('Deleted', failed=false)
            element.parentNode.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode.parentNode)
        }else if(r.detail){
            create_response('Room not found', failed=true)
        }else if(!r.success) {
            create_response('invalid room', failed=true)
        }
    })
    // remove element from room card
    

}
function refresh_code(element) {
    // Function to Refresh Room Code
    var room_code = element.getAttribute("room_code")
    var response = get_my_room("/api/user/refresh-code/" + room_code)
    response.then((r) =>{
        if(r.detail) {
            create_response("Invalid room (404)", failed=true)
        }
        if(r.success && r.room_code) {
            create_response("New room code generated!", failed=false)
            var child_nodes = element.parentNode.children
            for(i in child_nodes) {
                if(child_nodes[i].tagName == 'BUTTON') {
                    child_nodes[i].setAttribute("room_code", r.room_code)
                }
                if(child_nodes[i].tagName == 'A') {
                    child_nodes[i].href = "/chat/room/" + r.room_code
                }
                if(child_nodes[i].tagName == 'H5') {
                    child_nodes[i].children[0].setAttribute("room_code", r.room_code)
                }
            }
        }else{
            create_response("Invalid response", failed=true)
        }
    })
    

}

function create_next(url) {
    var next_position = document.getElementById("next-position")
    var element = `
    <button type="submit" class="btn btn-outline-dark" value="${url}" onclick="next_my_room(this)">Next</button>
    `
    next_position.innerHTML = element
}
function next_my_room(element) {
    var next_url = element.value 
    var response = get_my_room(next_url)
    response.then((r) => {
        show_room_card(r)
    })

}
async function get_my_room(custom_url=false) {
    if(custom_url) {
        url = custom_url
    }else{
        url = '/api/user/my-room'
    }
    var response = await fetch(url)
    return response.json()
}

function show_room_card(r) {
    if(r.next) {
        create_next(r.next)
    }else{
        document.getElementById("next-position").innerHTML = ""
    }
    if(r.results.length !== 0){
        for(i in r.results) {
            create_my_room_card(r.results[i].room_name, r.results[i].room_code)
        }
    }
}

if(room_row) {
    var response = get_my_room()   
    response.then((r)=> {
        show_room_card(r)
    })
}