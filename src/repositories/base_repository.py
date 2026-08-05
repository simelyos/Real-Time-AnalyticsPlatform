from abc import ABC
from psycopg import Connection
from psycopg import sql

import logging

logger = logging.getLogger(__name__)

class BaseRepository(ABC):

    table_name: str
    columns: list[str]

    def __init__(self, connection: Connection):
        self.connection = connection

    
    def bulk_insert(self, rows: list[tuple]):

        placeholders = sql.SQL(", ").join(
            sql.Placeholder() for _ in self.columns
        )

        query = sql.SQL("""
                    INSERT INTO {table}
                    ({columns})
                    VALUES ({values})
                """).format(
                    table=sql.Identifier(self.table_name),
                    columns=sql.SQL(", ").join(
                        map(sql.Identifier, self.columns)
                    ),
                    values=placeholders,
                )
        
        with self.connection.cursor() as cursor:
            cursor.executemany(query, rows)
            

        self.connection.commit()

    def save_many(self, models):

        rows = [
            model.to_tuple()
            for model in models
        ]
        try:
            self.bulk_insert(rows)
            logger.info("%s saved successfully.",self.table_name)
        except Exception as exception:
            logger.error("Failed to save %s. Following error occurred: %s",self.table_name,exception)

        
