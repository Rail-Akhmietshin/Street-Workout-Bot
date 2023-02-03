from .connect_with_db import DataBase


class Users(DataBase):

    async def create_table(self):
        connection = await self.connect()
        await connection.execute(
            '''CREATE TABLE IF NOT EXISTS users (
                    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
                    user_id BIGINT UNIQUE,
                    chat_id BIGINT UNIQUE,
                    name varchar(25) NOT NULL,
                    username varchar(255)
                )'''
            )
        await connection.close() 

    async def has_user(self, user_id):
        connection = await self.connect()
        try:
            user = await connection.fetchrow(
                f'SELECT user_id FROM users WHERE user_id = {user_id}'
            )
            await connection.close()
            return user['user_id']
        except:
            return False

    async def new_user(self, user_id, chat_id, name):
        connection = await self.connect()
        await connection.execute(
            '''INSERT INTO users(user_id, chat_id, name)
               VALUES ($1, $2, $3)''',
               int(user_id), int(chat_id), name
        )
        await connection.close()


        
