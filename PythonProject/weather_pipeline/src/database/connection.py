import psycopg2
from src.config.setting import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)