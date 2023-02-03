from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime, timedelta

from database.workout_time import WorkoutTime
from keyboards import kb_confirmation
from .states.all_states import Chat

from pydantic.error_wrappers import ValidationError

router = Router()


@router.callback_query( F.data.in_({'button_peoples'}) )
async def actual_users(callback : CallbackQuery, state : FSMContext):

    data = await state.get_data()
    lat = float(data["places"][data["cursor"]])
    get_data = await WorkoutTime().suitable_users_on_place(lat)
    users = [x for x in get_data if x["user_time"] > datetime.now() + timedelta(minutes=10)]
    users_buttons = InlineKeyboardBuilder()

    if users:
        for user_info in users:
            dt = user_info['user_time']
            datet = []
            for x in [dt.day, dt.month]:
                datet.append("0" + str(x) if x < 10 else str(x))
            
            hour_minute = f"{dt.hour}:{dt.minute}0" if dt.minute < 10 else f"{dt.hour}:{dt.minute}"

            users_buttons.row(InlineKeyboardButton(text=
                                                   f"{user_info['name']}.\n"
                                                   f"Записан {'.'.join(datet)} на: {hour_minute}\n",
                                 callback_data=f"user_{user_info['user_id']}"))
        users_buttons.adjust(1)
        await callback.message.answer("Актуальный список:",
                                      reply_markup=users_buttons.as_markup())
    else:
        await callback.message.answer("Сюда пока что никто не записался на тренировку. Стань первым! =)")
    await callback.answer()



@router.callback_query( F.data.startswith('user_') )
async def invited_on_chatting( callback: CallbackQuery, state: FSMContext):
    recipient_id = int(callback.data.split("_")[-1])
    data = await state.get_data()
    try:
        count = int(data[f"count_message_for_{recipient_id}"])
    except:
        count = 0
    
    if count < 1:
        await callback.message.answer(
            "Связаться с пользователем?",
            reply_markup=kb_confirmation.as_markup(resize_keyboard=True, one_time_keyboard=True)
        )
        await state.update_data( recipient_id = recipient_id )
        await state.set_state(Chat.first)
    else:
        await callback.message.answer(
            "На сегодня вы уже не можете отправить пользователю сообщение. Приходите завтра!",
        )
    await callback.answer()

@router.message(
    Chat.first,
    F.text.in_({"Подтвердить", "Отменить"})
)
async def chatting( message: Message, state: FSMContext):
    if message.text == "Подтвердить":
        await message.answer("Если у вашего профиля нет логина в формате '@login', то укажите в сообщении свои контакты для обратной связи")
        await message.answer("Введите сообщение ниже\n( !! Оно будет отправлено получателю !! )")
        await state.set_state(Chat.second)
    else:
        data = await state.get_data()
        data.pop("recipient_id")
        await state.set_data(data)
        await state.set_state(None)


@router.message(
    Chat.second,
    F.content_type.in_({'text', 'sticker'})
)
async def sender_message( message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    recipient_id = data["recipient_id"]
    async_data = {
        f"count_message_for_{recipient_id}" : "1",
        f"start_time_for_{recipient_id}" : datetime.now(),
    }

    await state.update_data( async_data )

    try:
        username = message.from_user.username
    except (ValidationError):
        username = message.from_user.first_name
    any_text = f"Отправлено от {username} через бота @StreetWrkBot для начала общения с вами!\n\n"

    await bot.send_message(
        chat_id = recipient_id,
        text = any_text + str(message.text),
    )
    await message.answer("Сообщение успешно отправлено получателю! Теперь вы можете продолжать пользоваться ботом =) ")
    await state.set_state(None)
    
