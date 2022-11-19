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
    message_id.innerHTML = ''
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
