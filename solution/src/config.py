from os import getenv

from dotenv import load_dotenv

load_dotenv()


class ServerSettings:
    SERVER_ADRESS: str = getenv("SERVER_ADRESS")
    SERVER_PORT: int = int(getenv("SERVER_PORT"))


class PostgresSettings:
    POSTGRES_USERNAME: str = getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD: str = getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = getenv("POSTGRES_PORT")
    POSTGRES_DATABASE: str = getenv("POSTGRES_DATABASE")


class JWTSettings:
    SECRET_KEY: str = getenv("RANDOM_SECRET")
    ALGORITHM: str = "HS256"
    ACCSES_TOKEN_EXPIRE_MINUTES = 30


server_settings = ServerSettings()
postgres_settings = PostgresSettings()
jwt_settings = JWTSettings()
