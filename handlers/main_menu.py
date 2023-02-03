from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from .states.all_states import Workout
from aiogram.types import Message
from datetime import datetime

import asyncio

from keyboards import kb_menu, kb_places, kb_districts
from constants import time_format
from database.workout_time import WorkoutTime

router = Router()

@router.message( F.text == "Главное меню" )
@router.message( Command(commands=['menu']) )
async def main_menu( message: Message):
#    await WorkoutTime().expired_workouts(message.from_user.id)

    await message.answer('Добро пожаловать в главное меню!')
    await asyncio.sleep(1.5)
    await message.answer(
        text='Ты можешь выбрать площадку для твоих тренировок, которая будет тебе по душе,'
        'а так же позвать ещё кого-нибудь,'
        'чтобы тебе не было скучно :)',
        reply_markup=kb_menu.as_markup(resize_keyboard=True)
    )





@router.message(F.text == "Выбор площадки")
async def choice_place( message: Message, state: FSMContext):
    await message.answer(
        "Какую площадку предпочтёшь?",
        reply_markup = kb_places.as_markup(resize_keyboard=True))
    
    data = await state.get_data()
    necc = {}
    for key, value in data.items():
        if key.startswith("start_time_for_"):
            if (datetime.now() - datetime.strptime(value, time_format)).days < 1:
                necc[key] = datetime.strftime(value, time_format)
        elif key.startswith("count_message_for_"):
            necc[key] = value
        continue
    
    await state.set_data(necc)
    await state.set_state(Workout.type_place)




@router.message(
    Workout.type_place,
    F.text.in_({'Футбольное поле','Баскетбольная площадка', 'Воркаут-площадка', 'Особое'}),
)
async def type_place( message: Message, state: FSMContext):
    await state.update_data(type_place = message.text)
    await message.answer(
        "В каком районе?",
        reply_markup = kb_districts.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )

    await message.answer( "К сожалению, пока доступен только Вахитовский район :(" )
    await state.set_state(Workout.finish)





    


