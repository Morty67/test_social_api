from datetime import datetime

import json
import random

import requests
from faker import Faker

from config import password_context

fake = Faker()

created_post_ids = (
    []
)  # Create an empty list to store the IDs of created posts

LOGIN_URL = "http://127.0.0.1:8000/users/login/"
CREATE_POST_URL = "http://127.0.0.1:8000/posts/create_post/"
LIKE_POST_URL = f"http://127.0.0.1:8000/likes/like_post/"
CREATE_USER_URL = "http://127.0.0.1:8000/users/create_user/"


def login_user(username, password):
    login_data = {"username": username, "password": password}

    response = requests.post(
        LOGIN_URL, data=login_data
    )  # Make a POST request to log in

    if response.status_code == 200:
        jwt_token = response.json().get(
            "access_token"
        )  # Extract JWT token if login is successful
        print(f"User {username} successfully logged in")
        return jwt_token  # Return the JWT token if successful
    else:
        print(f"Error with user login {username}: {response.text}")
        return None


def create_post(jwt_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
    }

    post_data = {
        "title": fake.sentence(),
        "content": fake.paragraph(),
        "created_at": datetime.utcnow().isoformat(),
    }

    response_create_post = requests.post(
        CREATE_POST_URL, data=json.dumps(post_data), headers=headers
    )

    if response_create_post.status_code == 200:
        # Успішно створено пост
        created_post = response_create_post.json()
        print(f"Post successfully created: {created_post}")
        return created_post[
            "id"
        ]  # Return the ID of the created post if successful
    else:
        print(f"Error creating a post: {response_create_post.text}")


def like_post(jwt_token, post_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
    }

    like_data = {"post_id": post_id}

    response_like_post = requests.post(
        f"{LIKE_POST_URL}{post_id}", json=like_data, headers=headers
    )

    if response_like_post.status_code == 200:
        # Успішно створено лайк
        created_like = response_like_post.json()  # Extract the created like
        print(f"Like successfully created: {created_like}")
    else:
        print(f"Error when creating a like: {response_like_post.text}")


def create_and_add_data():
    with open("bot_config.json", "r") as config_file:
        config = json.load(
            config_file
        )  # Read user configuration data from a JSON file

    number_of_users = config["number_of_users"]  # Extract the number of users
    max_posts_per_user = config[
        "max_posts_per_user"
    ]  # Extract max posts per user
    max_likes_per_user = config[
        "max_likes_per_user"
    ]  # Extract max likes per user

    headers = {"Content-Type": "application/json"}  # Define request headers

    for _ in range(number_of_users):
        username = fake.user_name()
        full_name = fake.name()
        email = fake.email()
        password = password_context.hash("string")

        user_data = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": password,
        }
        response_create_user = requests.post(
            CREATE_USER_URL, json=user_data, headers=headers
        )

        if response_create_user.status_code == 200:
            created_user = (
                response_create_user.json()
            )  # Extract the created user
            print(f"User {username} successfully established: {created_user}")
            print("________________________")

            jwt_token = login_user(
                username, password
            )  # Log in the user and get JWT token
            if jwt_token:
                print(f"JWT token successfully received: {jwt_token}")
                print("________________________")
                for _ in range(max_posts_per_user):
                    created_post_id = create_post(
                        jwt_token
                    )  # Create a post and get its ID
                    if created_post_id:
                        created_post_ids.append(
                            created_post_id
                        )  # Append post ID to the list
                    print("________________________")
                    for _ in range(max_likes_per_user):
                        if created_post_ids:
                            random_post_id = random.choice(
                                created_post_ids
                            )  # Choose a random post ID
                            like_post(
                                jwt_token, random_post_id
                            )  # Like the post
                            print("________________________")

        else:
            print(
                f"Error creating a user {username}: {response_create_user.text}"
            )


if __name__ == "__main__":
    create_and_add_data()
