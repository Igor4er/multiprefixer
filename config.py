import os
from dotenv import load_dotenv
load_dotenv(".env")
BASE_DIRECTORY = os.getenv("BASE_DIR")


class Configuration(object):
    DEBUG = os.getenv("APP_DEBUG")
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
