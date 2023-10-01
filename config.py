from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
