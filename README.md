# Vara_backend

A video site backend.

## Required functions

- [x] User
  - [x] Register
  - [x] Login
  - [x] Logout
  - [x] Profile
    - [x] Avatar
    - [x] Header
    - [x] Description
    - [x] Comments
  - [x] Following
  - [x] Followers
  - [x] Friends
  - [x] Posts
    - [x] Comments
  - [x] Playlists
  - [x] Messages
  - [x] Notifications
  - [x] Notifications settings
  - [ ] Blacklist tags
- [x] Videos
  - [x] Comments
  - [x] Views
  - [x] Likes
  - [x] Ratings
  - [x] Thumbnails
    - [x] List view
    - [x] Video thumbnails * 12
- [x] Images
  - [x] Comments
  - [x] Views
  - [x] Likes
  - [x] Ratings
  - [x] Thumbnails
    - [x] List view
    - [x] Large image thumbnail * 1
- [x] Tags
- [x] Forums
  - [x] Threads
    - [x] Posts
- [ ] Trending

## run server

local

```
python manage.py runserver
```

## start database

start db

```
docker-compose -f docker-mysql.yml up -d
```

stop db

```
docker-compose -f docker-mysql.yml down
```


# model

make a migration from model

```
python manage.py makemigrations app
```

run migrate

```
python manage.py migrate
```

display migrate sql

```
python manage.py sqlmigrate myapp 0001
```

## dotenv

```
SECRET_KEY=
DEBUG=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```