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

function update_user() {
    var data = get_fields()
    var z = post_data('/api/user/profile', data)
    z.then((r) => {
        console.log(r)
    })
}

function create_response(text, failed=false) {
    var div = document.createElement("div")
    if(failed){
        div.className = "alert alert-danger"
        div.innerHTML = text 
    }else{
        div.className = "alert alert-success"
        div.innerHTML = text
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
    message_id.innerHTML = ""

}

function register_user() {
    message_id.innerHTML = ""
    let data = get_fields()
    post_data(register_url, data).then((response) => {
        if(response.success) { 
            create_response('Registered, you can login now')
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