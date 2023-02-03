from .connect_with_db import DataBase
from constants import place


class Places(DataBase):

    async def create_table(self):
        connection = await self.connect()
        await connection.execute(
            'CREATE TABLE IF NOT EXISTS place ('
                'id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),'
                'file_id varchar(255) UNIQUE NOT NULL,'
                'district varchar(30) NOT NULL,'
                'about VARCHAR(255) NOT NULL,'
                'lat DOUBLE PRECISION NOT NULL,'
                'lon DOUBLE PRECISION NOT NULL,'
                'type_place INTEGER NOT NULL'
            ')'
        )     
        await connection.close()

    async def update_table(self, file_id, about, district, lat, lon, type):
        connection = await self.connect()
        await connection.execute(
            'INSERT INTO place(file_id, district, about, lat, lon, type_place)'
                'VALUES ($1, $2, $3, $4, $5, $6)',
            str(file_id), str(district), about, lat, lon, type
        )
        await connection.close()

    async def get_places(self, type_place):
        connection = await self.connect()
        
        try:
            match = await connection.fetch( 
                '''SELECT lat
                FROM place
                WHERE type_place = $1
                GROUP BY lat
                ORDER BY random()''',
                place[type_place]
            )
            return [x[0] for x in match]
        finally:
            await connection.close()

    async def get_place(self, lat: float):
        connection = await self.connect()

        try:
            match = await connection.fetch(
                '''SELECT file_id, lat, lon, about
                FROM place
                WHERE lat = $1''',
                float(lat)
            )
            return match
        finally:
            await connection.close()
