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
- Messages saved to database
- Messages from not logged in user will no saved to database

### Screenshots
Room Chat
![chat](https://user-images.githubusercontent.com/70421698/202155793-8aaba456-1535-4eb7-bdfe-a97fc699697f.png)

Create Room
![create-room](https://user-images.githubusercontent.com/70421698/202155806-2e96a929-119c-411e-bf20-d81bcfefd192.png)

Login Page
![login](https://user-images.githubusercontent.com/70421698/202155809-e9392aaf-5651-487b-85b5-da8940fee6ba.png)

Register Page
![register](https://user-images.githubusercontent.com/70421698/202155814-c908c8c7-ee36-467c-b5c8-d45803a34b0b.png)

Room index
![room](https://user-images.githubusercontent.com/70421698/202155818-24e0f40a-cfa5-4f67-a15e-56fe30641a06.png)
