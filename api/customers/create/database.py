import os
import pymysql
from dotenv import load_dotenv
from pathlib import Path

# find project root automatically
env_path = Path(__file__).resolve().parents[3] / ".env"

load_dotenv(dotenv_path=env_path)


def get_connection():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection