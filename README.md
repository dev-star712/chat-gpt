# Chat App
Group chat app built with Django, django-channels, and rest_framework 

## Table Of Contents

- [Chat App](#chat-app)
  - [Table Of Contents](#table-of-contents)
    - [Installation](#installation)
    - [Setup](#setup)
    - [Features](#features)
    - [Screenshots](#screenshots)

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
- Authenticated user can generate new room code, and delete their own room
- Messages saved to database
- Messages from not logged in user will no saved to database

### Screenshots
Chat Section  

Chat template i got from https://github.com/pamekasancode/webchat-js/tree/master (thx a lot for this guy)

![Screenshot 2022-11-25 152320](https://user-images.githubusercontent.com/70421698/203936238-2ef6289e-9ffa-46b5-b8c3-866601eb3baa.png)
![Screenshot 2022-11-25 152358](https://user-images.githubusercontent.com/70421698/203936248-02c64ef6-d633-4ea3-9c52-967f046f9fef.png)
![Screenshot 2022-11-25 152419](https://user-images.githubusercontent.com/70421698/203936255-b64e2a1b-032a-4eb6-ba8c-0ed0c7d032b8.png)
![Screenshot 2022-11-25 152441](https://user-images.githubusercontent.com/70421698/203936261-994d7eed-614b-4213-b29c-393721c5b264.png)