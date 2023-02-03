from aiogram import Router, F
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from database.users import Users
from .states.all_states import User


router = Router()



@router.message(Command(commands=["start", "about"]))
async def authentication(message: Message, state: FSMContext):

    await message.answer(
        'Привет!\n'\
        'Это бот для тренировок на улице\n'\
        'Побежали тренироваться!\n'
    )
    await message.delete()

    

    if await Users().has_user(message.from_user.id):
        await message.answer(
            "Так как ты уже зарегистрирован, то давай с тобой перейдём в главное меню!\n"
            "Введи команду /menu",
        )
    
    elif not message.from_user.first_name:
        await message.answer("Давай с тобой познакомимся! Как тебя зовут?")
        await state.set_state(User.first_name)
    
    else:
        await Users().new_user(
            message.from_user.id,
            message.chat.id,
            message.from_user.first_name
        )
        await message.answer(
            "Отлично! Ты успешно зарегистрировался! А теперь вперед к функционалу бота с помощью команды /menu"
        )




@router.message(
    User.first_name,
    F.text.regexp(r'^[а-яА-Я]{2,20}')
)
async def input_first_name(message: Message):
    await Users().new_user(
            message.from_user.id,
            message.chat.id,
            message.text,
    )
    await message.answer(
            "Отлично! Ты успешно зарегистрировался! А теперь вперед к функционалу бота с помощью команды /menu"
        )

