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
Chat 
![Screenshot_20221119_063958](https://user-images.githubusercontent.com/70421698/202820949-720ab5eb-7576-48a1-afe0-62124a40fa0d.png)

Room Chat
![Screenshot_20221117_055340](https://user-images.githubusercontent.com/70421698/202428160-357fb7fe-0a11-4e56-9621-78257ff5428c.png)

Create Room

![Screenshot_20221117_055436](https://user-images.githubusercontent.com/70421698/202428150-b9d92bd2-07b9-44d7-8db1-3256103a5266.png)

Login Page
![login](https://user-images.githubusercontent.com/70421698/202155809-e9392aaf-5651-487b-85b5-da8940fee6ba.png)

Register Page
![register](https://user-images.githubusercontent.com/70421698/202155814-c908c8c7-ee36-467c-b5c8-d45803a34b0b.png)
