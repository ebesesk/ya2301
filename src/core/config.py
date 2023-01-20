import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Settings:
    TITLE = os.getenv("TITLE")
    VERSION = os.getenv("VERSION")
    DESCRIPTION = os.getenv("DESCRIPTION")
    NAME = os.getenv("NAME")
    EMAIL = os.getenv("EMAIL")
    
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

settings = Settings()