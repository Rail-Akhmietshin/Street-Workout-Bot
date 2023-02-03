from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.fsm.context import FSMContext

from datetime import datetime, timedelta, date, time


from .states.all_states import Workout
from database.workout_time import WorkoutTime
from .workout_menu import get_one_place
from keyboards import kb_confirmation
from constants import dates, time_format


import asyncio

router = Router()


async def valid(input_date, input_time):

    hour, minute = input_time.split(":")

    input_time = input_time.split(":")

    try:
        days = int(dates[input_date])
    except KeyError:
        return False
    act_t = datetime.now() + timedelta(hours=2)

    user_t = datetime.combine(
        date = date.today() + timedelta(days=days),
        time = time(hour = int(hour), minute = int(minute))
    )

    tt = datetime.now() + timedelta(days=4)
    valid_t = datetime(tt.year, tt.month, tt.day)

    if act_t <= user_t < valid_t:
        return user_t

    return False



@router.message(
    Workout.date,
    F.text.regexp(r'^[а-яА-Я]+')
)
async def date_date(message : Message, state : FSMContext):
    if message.text == "Отмена":
        await state.finish()

        data = await state.get_data()
        await get_one_place(message, data["places"], data["cursor"])
    else:
        await state.update_data(day=str(message.text))
        await message.answer(
                            "Введите время вашей тренировки на данной площадке не раньше, чем за 2 часа до начала ("
                            "Формат вида: '03:25')",
                            reply_markup=ReplyKeyboardRemove()
                            )

        await state.set_state(Workout.time_time)


@router.message(
    Workout.time_time,
    F.text.regexp(r"^[0-9]{1,2}:[0-9]{2}")
)
async def time_time(message : Message, state : FSMContext):

    await state.update_data(hour_minutes=str(message.text))
    data = await state.get_data()

    check = await valid(data["day"], data["hour_minutes"])
    if check:
        await state.update_data(full_date=datetime.strftime(check, time_format))
        await message.answer("Вы уверены, что хотите записаться на текущее время и дату? Отменить будет невозможно",
                             reply_markup=kb_confirmation.as_markup(resize_keyboard=True))
        await state.set_state(Workout.record_confirmation)
    else:
        await message.answer("Неверный ввод. Повторите попытку!")
        await state.set_state(Workout.time_time)
        await asyncio.sleep(2)
        
        await get_one_place(message, data["places"], data["cursor"])




@router.message(
    Workout.record_confirmation,
    F.text.in_({'Подтвердить', 'Отменить'})
)
async def confirmation(message : Message, state : FSMContext):

    data = await state.get_data()

    if message.text == "Подтвердить":
        date = await state.get_data()
        await message.answer(
            f"Вы успешно записаны на {date['day'].lower()} в {date['hour_minutes']}!",
            reply_markup=ReplyKeyboardRemove())
        
        await WorkoutTime().new_workout(data["places"][data["cursor"]], message.from_user.id, date["full_date"])
        await asyncio.sleep(2)
    else:
        await state.clear()

        await get_one_place(message, data["places"], data["cursor"])
