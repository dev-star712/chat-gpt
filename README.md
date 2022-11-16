# Chat App
Group chat app built with Django, django-channels, and rest_framework 

## Table Of Contents

- [Chat App](#chat-app)
  - [Table Of Contents](#table-of-contents)
    - [Installation](#installation)
    - [Setup](#setup)
    - [Features](#features)

### Installation
- Clone this repository https://github.com/gibran-abdillah/chat-app
```sh
git clone https://github.com/gibran-abdillah/chat-app
cd chat-app
```
- Activate the local environment
```sh
virtualenv env
source env/bin/activate
```
- Install the requirements
```sh
pip3 install -r requirements.txt
```
- Migrate the database
```sh
./manage.py makemigrations
./manage.py migrate
```

### Setup 
Go to app/settings.py to set your Redis url
```py
CHANNEL_LAYERS = {
        "default":{
            "BACKEND":"channels_redis.core.RedisChannelLayer",
            "CONFIG":{
                "hosts":[('localhost', 6379)],
            }
        },
}
```
You can run the server by using command
```sh
./manage.py runserver
```

### Features
- Login and Register
- Any logged in user can create a room
- Messages saved to database
- Messages from not logged in user will no saved to database
