import asyncio
from aiogram import Router, F
from aiogram.types import InputMediaPhoto, Message, CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

from .states.all_states import Workout
from database.place import Places

from keyboards import *

router = Router()



async def get_one_place(message: Message, places, cursor):
    current_place = await Places().get_place(float(places[cursor]))

    media = [InputMediaPhoto(media=current_place[0][0], caption=current_place[0][-1])]
    for j in range(1, len(current_place)):
        media.append(InputMediaPhoto(media=current_place[j][0]))

    await message.answer_media_group(media)
    await message.answer(
         text='Меню:', 
         reply_markup=await kb_search(cursor, len(places) - 1)
    )

    return media


@router.message(
    Workout.finish,
    F.text.in_({'Вахитовский'})
)
async def workouts_main_menu( message: Message, state: FSMContext):
    data = await state.get_data()

    suitable_places = await Places().get_places(data["type_place"])

    
    await state.update_data( places = suitable_places, cursor = 0)

    await get_one_place(message, suitable_places, 0)
    


@router.callback_query(F.data.in_({'button_next', "button_previous"}))
async def previous_or_next_place( callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[-1]
    data = await state.get_data()
    data["cursor"] += 1 if action == "next" else -1

    await state.update_data(cursor = data["cursor"])
    
    await get_one_place(callback.message, data["places"], data["cursor"])

    await callback.answer()

    


@router.callback_query(F.data.in_({'button_geopos', "button_record"}))
async def geopos_peoples_record( callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[-1]
    data = await state.get_data()

    if action == "geopos":
        current_place = await Places().get_place(float(data["places"][data["cursor"]]))
        await callback.message.answer_location(latitude=current_place[0][1], longitude=current_place[0][2])
        await callback.answer()
    
    if action == "record":
        
        await callback.message.answer(
            "Можно записаться не раньше, чем за 4 дня до тренировки",
        )
        await asyncio.sleep(1)
        await callback.message.answer(
            "Введите день вашей тренировки",
            reply_markup=kb_date.as_markup(resize_keyboard=True)
        )
        await state.set_state(Workout.date)

    await callback.answer()


