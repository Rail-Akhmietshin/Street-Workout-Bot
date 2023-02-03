import asyncpg
import os

class DataBase:
    
    async def connect(self):
        self.connection = await asyncpg.connect(
            database = str(os.environ.get("POSTGRES_DB")),
            user = str(os.environ.get("POSTGRES_USER")),
            password = str(os.environ.get("POSTGRES_PASSWORD")),
            host = os.environ.get("POSTGRES_HOST"),
            port = os.environ.get("POSTGRES_PORT")
        )
        return self.connection
