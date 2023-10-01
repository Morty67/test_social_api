from fastapi import HTTPException
from app.auth.security import verify_password, create_jwt_token
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.serializers.user_serializer import UserCreate, UserResponse
from config import password_context


class UserService:
    """
    Service class for user-related operations including registration, login, and information retrieval.

    This class provides methods to register new users, authenticate users during login,
    and retrieve last login and last request timestamps for users.

    Attributes:
        user_repo (UserRepository): An instance of UserRepository for database operations related to users.
    """

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Registers a new user with the provided data.

        Args:
            user_data (UserCreate): The data for creating the new user.

        Returns:
            UserResponse: An instance of UserResponse containing the details of the registered user.

        Raises:
            HTTPException: If a user with the same username or email already exists.
        """
        if await self.user_repo.exists_by_username(user_data.username):
            raise HTTPException(
                detail="User with this username already exists",
                status_code=400,
            )

        if await self.user_repo.exists_by_email(user_data.email):
            raise HTTPException(
                detail="User with this email already exists",
                status_code=400,
            )

        hashed_password = password_context.hash(user_data.password)

        new_user = User(
            username=user_data.username,
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        await self.user_repo.save(new_user)

        return UserResponse(
            id=new_user.id,
            username=new_user.username,
            full_name=new_user.full_name,
            email=new_user.email,
        )

    async def login_user(self, username: str, password: str) -> str:
        """
        Authenticates a user during login and generates an access token.

        Args:
            username (str): The username of the user trying to log in.
            password (str): The password provided by the user.

        Returns:
            str: The JWT access token if login is successful.

        Raises:
            HTTPException: If the username or password is incorrect.
        """
        user = await self.user_repo.get_user_by_username(username)
        if not user or not await verify_password(
            password, user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
            )

        await self.user_repo.update_last_login(user)
        await self.user_repo.update_last_request(user)

        access_token = await create_jwt_token({"sub": user.username})
        return access_token

    async def get_last_login(self, user_id: int):
        """
        Retrieves the timestamp of the last login for the specified user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            datetime: The timestamp of the last login.

        Raises:
            HTTPException: If the user specified by user_id is not found.
        """
        last_login = await self.user_repo.get_last_login(user_id)
        return last_login

    async def get_last_request(self, user_id: int):
        """
        Retrieves the timestamp of the last request made by the specified user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            datetime: The timestamp of the last request.

        Raises:
            HTTPException: If the user specified by user_id is not found.
        """
        last_request = await self.user_repo.get_last_request(user_id)
        return last_request
