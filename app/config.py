from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))

# DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    DATABASE_TYPE: str
    DATABASE_USERNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: int
    DATABASE_HOST: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
