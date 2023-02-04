import asyncpg
import os

class DataBase:
    
    async def connect(self):
        self.connection = await asyncpg.connect(
            database = str(os.environ.get("POSTGRES_DB")),
            user = str(os.environ.get("POSTGRES_USER")),
            password = str(os.environ.get("POSTGRES_PASSWORD")),
            host = "db",
            port = os.environ.get("POSTGRES_PORT", default="5432")
        )
        return self.connection
