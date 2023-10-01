# FastAPI for Social Media API
This project is the server-side component of a web application that provides an API for managing users and posts. FastAPI framework is used to create API endpoints, and the data is stored in a PostgreSQL database. Additionally, JWT-based security is implemented for authentication.
## Technologies Used

*  Backend: FastAPI.
*  Database: Async PostgreSQL.
*  Security : JWT
*  Docker for containerization.


## Installing / Getting started:
```shell
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/test_social_api/tree/developer
Python 3.11.3 must be installed

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt

Your settings for DB in .env file:

DB_HOST=YOUR DB_HOST
DB_PORT=YOUR DB_PORT
DB_NAME=YOUR DB_NAME
DB_USER=YOUR DB_USER
DB_PASS=YOUR DB_PASS

JWT_SECRET_KEY=YOUR JWT_SECRET_KEY
JWT_ALGORITHM in .env.sample

BASE_URL=your url like http://127.0.0.1:8000/ 

alembic upgrade head
uvicorn app.main:app --reload

```

## How to get access
Domain:
*  localhost:8000 or 127.0.0.1:8000 (127.0.0.1:8000/docs)

## Run bot.py
* python bot.py


## Run Docker 🐳
Docker must be installed :
* docker-compose up --build
## Run bot.py in Docker:
* docker exec -it container id bash
* python bot.py
```shell


## API Features:
*  User signup
*  User login
*  Post creation
*  Post like
*  Post unlike
*  Analytics about how many likes were made. The API return analytics aggregated by day.
*  User activity: an endpoint that will show when the user last logged in and when they made their last request to the service.  
*  API documentation is available at http://localhost:8000/docs when the application is running. You can explore and test the endpoints using the Swagger UI.


## Bot.py Features:
* The bot reads configuration rules from the bot_config.json file

* User registration:
* The bot registers users based on the number of users specified in the configuration.
* Each user has a unique profile.

* Creating random posts:

* After registration, each user creates a random number of posts.
* The number of posts corresponds to the max_posts_per_user specified in the configuration.
* The content of the posts can be arbitrary.

* Like posts:

* After registration and publishing, the bot randomly likes posts.
* A user can like a post only once, or like or unlike it.
* The number of likes from each user corresponds to the max_likes_per_user specified in the configuration.