from datetime import datetime
import json
import random
import requests
from faker import Faker
from config import password_context
import logging
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

logging.basicConfig(level=logging.INFO)


class Bot:
    """
    A bot for simulating user actions, including creating users, posts, and likes.

    This class provides methods for interacting with a web API to create users, log in users,
    create posts, and like posts. It uses the Faker library to generate fake user data and
    posts. The bot reads configuration data from a 'bot_config.json' file.

    Attributes:
        fake (Faker): An instance of the Faker class for generating fake data.
        created_post_ids (list): A list to store the IDs of created posts.
        LOGIN_URL (str): The URL for user login.
        CREATE_POST_URL (str): The URL for creating a post.
        LIKE_POST_URL (str): The URL for liking a post.
        CREATE_USER_URL (str): The URL for creating a user.
    """

    def __init__(self):
        self.fake = Faker()
        self.created_post_ids = []

        self.LOGIN_URL = f"{BASE_URL}users/login/"
        self.CREATE_POST_URL = f"{BASE_URL}posts/create_post/"
        self.LIKE_POST_URL = f"{BASE_URL}likes/like_post/"
        self.CREATE_USER_URL = f"{BASE_URL}users/create_user/"

    def login_user(self, username, password):
        """
        Logs in a user with the provided username and password.

        Args:
            username (str): The username of the user to log in.
            password (str): The password of the user.

        Returns:
            str: The JWT token if login is successful, None otherwise.
        """
        login_data = {"username": username, "password": password}
        response = requests.post(self.LOGIN_URL, data=login_data)
        if response.status_code == 200:
            jwt_token = response.json().get("access_token")
            logging.info(f"User {username} successfully logged in")
            return jwt_token
        else:
            logging.error(
                f"Error with user login {username}: {response.text}"
            )
            return None

    def create_post(self, jwt_token):
        """
        Creates a new post with random content.

        Args:
            jwt_token (str): The JWT token for authentication.

        Returns:
            int: The ID of the created post if successful, None otherwise.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt_token}",
        }
        post_data = {
            "title": self.fake.sentence(),
            "content": self.fake.paragraph(),
            "created_at": datetime.utcnow().isoformat(),
        }
        response_create_post = requests.post(
            self.CREATE_POST_URL, data=json.dumps(post_data), headers=headers
        )
        if response_create_post.status_code == 200:
            created_post = response_create_post.json()
            logging.info(f"Post successfully created: {created_post}")
            return created_post["id"]
        else:
            logging.error(
                f"Error creating a post: {response_create_post.text}"
            )

    def like_post(self, jwt_token, post_id):
        """
        Likes a post with the given ID.

        Args:
            jwt_token (str): The JWT token for authentication.
            post_id (int): The ID of the post to like.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt_token}",
        }
        like_data = {"post_id": post_id}
        response_like_post = requests.post(
            f"{self.LIKE_POST_URL}{post_id}", json=like_data, headers=headers
        )
        if response_like_post.status_code == 200:
            created_like = response_like_post.json()
            logging.info(f"Like successfully created: {created_like}")
        else:
            logging.error(
                f"Error when creating a like: {response_like_post.text}"
            )

    def create_and_add_data(self):
        """
        Creates users, logs them in, creates posts, and likes posts based on configuration data.
        """
        with open("bot_config.json", "r") as config_file:
            config = json.load(config_file)

        number_of_users = config["number_of_users"]
        max_posts_per_user = config["max_posts_per_user"]
        max_likes_per_user = config["max_likes_per_user"]

        headers = {"Content-Type": "application/json"}

        for _ in range(number_of_users):
            username = self.fake.user_name()
            full_name = self.fake.name()
            email = self.fake.email()
            password = password_context.hash("string")

            user_data = {
                "username": username,
                "full_name": full_name,
                "email": email,
                "password": password,
            }
            response_create_user = requests.post(
                self.CREATE_USER_URL, json=user_data, headers=headers
            )

            if response_create_user.status_code == 200:
                created_user = response_create_user.json()
                logging.info(
                    f"User {username} successfully established: {created_user}"
                )
                logging.info("________________________")

                jwt_token = self.login_user(username, password)
                if jwt_token:
                    logging.info(
                        f"JWT token successfully received: {jwt_token}"
                    )
                    logging.info("________________________")
                    for _ in range(max_posts_per_user):
                        created_post_id = self.create_post(jwt_token)
                        if created_post_id:
                            self.created_post_ids.append(created_post_id)
                        logging.info("________________________")
                        for _ in range(max_likes_per_user):
                            if self.created_post_ids:
                                random_post_id = random.choice(
                                    self.created_post_ids
                                )
                                self.like_post(jwt_token, random_post_id)
                                logging.info("________________________")
            else:
                logging.error(
                    f"Error creating a user {username}: {response_create_user.text}"
                )


if __name__ == "__main__":
    bot = Bot()
    bot.create_and_add_data()
