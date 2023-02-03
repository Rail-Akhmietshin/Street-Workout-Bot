from aiogram import Router, F
from aiogram.types import Message
from database.place import Places


router = Router()

@router.message(F.photo)
async def upload_photo( message: Message ) -> None:

    result = await Places().update_table(
        file_id = message.photo[-1].file_id,
        about = "Футбольное поле",
        district = "Вахитовский",
        lat = 55.789981,
        lon = 49.139845,
        type = 2,
    )

    if result:
        await message.answer("Площадка успешно загружена!")
    
    
