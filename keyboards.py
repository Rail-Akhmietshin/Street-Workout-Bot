from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


''' Главное меню '''


kb_menu = ReplyKeyboardBuilder()
kb_menu.add(KeyboardButton(text="Выбор площадки")).add(KeyboardButton(text="Мои записи на тренировки"))
kb_menu.adjust(1)


''' Типы площадок '''

kb_places = ReplyKeyboardBuilder()
kb_places.add(KeyboardButton(text='Футбольное поле')).add(KeyboardButton(text='Воркаут-площадка')).add(KeyboardButton(text='Баскетбольная площадка')).add(KeyboardButton(text='Особое'))
kb_places.adjust(2)


''' Районы '''


kb_districts = ReplyKeyboardBuilder()
kb_districts.add(KeyboardButton(text="Вахитовский"))#.add(KeyboardButton(text="Приволжский"))
kb_districts.adjust(2)



''' Следующая/Предыдущая площадка'''

two_buttons = [
        [
            InlineKeyboardButton(
                text="Следующая", 
                callback_data='button_next'
            ),
            InlineKeyboardButton(
                text="Предыдущая", 
                callback_data='button_previous'
            )
        ],
    ]
kb_two_buttons = InlineKeyboardMarkup(inline_keyboard=two_buttons)



async def kb_search(cursor, end):
    builder = InlineKeyboardBuilder()
    
    if not cursor:
        builder.add(two_buttons[0][0])
    elif cursor == end:
        builder.add(two_buttons[0][-1])
    else:
        builder.add(two_buttons[0][0])
        builder.add(two_buttons[0][-1])
    builder.row(InlineKeyboardButton(text="Местоположение", callback_data='button_geopos'))
    builder.row(InlineKeyboardButton(text="Кто здесь уже занимается", callback_data='button_peoples'))
    builder.row(InlineKeyboardButton(text="Записаться на тренировку", callback_data="button_record"))

    builder.adjust(2)
    return builder.as_markup()


''' Дата тренировки '''


kb_date = ReplyKeyboardBuilder()

kb_date.add(
    KeyboardButton(text="Сегодня")).add(
        KeyboardButton(text="Завтра")).add(
            KeyboardButton(text="Послезавтра")).add(
                KeyboardButton(text="Послепослезавтра")).add(
                    KeyboardButton(text="Отмена"))

kb_date.adjust(2)


''' Подтверждение тренировки'''


kb_confirmation = ReplyKeyboardBuilder()
kb_confirmation.add(KeyboardButton(text="Подтвердить")).add(KeyboardButton(text="Отменить"))
kb_confirmation.adjust(2)




