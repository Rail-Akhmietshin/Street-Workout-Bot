from .connect_with_db import DataBase
from datetime import datetime
from constants import time_format

class WorkoutTime(DataBase):
    
    async def create_table(self):
        connection = await self.connect()
        await connection.execute(
            '''CREATE TABLE IF NOT EXISTS time (
                id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
                user_id BIGINT,
                user_time timestamp without time zone,
                coords int,
                CONSTRAINT FK_user FOREIGN KEY (user_id) REFERENCES users(user_id),
                CONSTRAINT FK_coords FOREIGN KEY (coords) REFERENCES place(id)
            )'''
        )
        await connection.close()    
    async def new_workout(self, lat, user_id, user_time):
        connection = await self.connect()
        
        match = await connection.fetchrow(
            '''SELECT id
            FROM place
            WHERE lat = $1
            LIMIT 1''',
            lat
        )
        await connection.execute(
            '''INSERT INTO time (user_id, user_time, coords)
            VALUES
            ($1, $2, $3)''',
            user_id, datetime.strptime(user_time, time_format), match[0]
        )

        await connection.close()

    async def suitable_users_on_place(self, lat):
        connection = await self.connect()

        try:
            match = await connection.fetch('''SELECT users.name, time.user_time, time.user_id
                                    FROM time
                                    LEFT JOIN place ON time.coords = place.id
                                    LEFT JOIN users ON time.user_id = users.user_id
                                    WHERE lat = $1''',
                                    lat)
            return match
        finally:
            await connection.close()

    async def expired_workouts(self, user_id):
        connection = await self.connect()

        match = await connection.fetch(
            '''SELECT id, user_time
            FROM time
            WHERE user_id = $1
            ''',
            user_id
        )
        time_now = datetime.now()
        print(match[0][1])
        i = 0
        for id, time in match[i]:
            print(id, time, sep="\n")
            converting = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - converting).days < 0:
                await connection.execute( "DELETE FROM time WHERE id = $1", id )
            i += 1
            continue
        await connection.close()
