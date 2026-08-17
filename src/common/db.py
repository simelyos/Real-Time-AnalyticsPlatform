import psycopg
from psycopg.rows import dict_row

from src.common.config import DB_CONFIG


def get_connection():
    return psycopg.connect(
        **DB_CONFIG,
        row_factory=dict_row
    )



def get_connection_analytics():

    analytics_config= {
            "host":"localhost",
            "port":5433,
            "dbname":"analytics",
            "user":"postgres",
            "password":"postgres"
        }
    
    return psycopg.connect(
        **analytics_config,
        row_factory=dict_row
    )