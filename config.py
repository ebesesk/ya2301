import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Settings:
    TITLE = os.getenv("TITLE")
    VERSION = os.getenv("VERSION")
    DESCRIPTION = os.getenv("DESCRIPTION")
    NAME = os.getenv("NAME")
    EMAIL = os.getenv("EMAIL")

setting = Settings()