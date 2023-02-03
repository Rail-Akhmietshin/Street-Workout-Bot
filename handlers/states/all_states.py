from aiogram.dispatcher.fsm.state import StatesGroup, State


class User(StatesGroup):
    first_name = State()

class Main(StatesGroup):
    menu = State()

class MyWorkouts(StatesGroup):
    my_workouts = State()

class Workout(StatesGroup):
    type_place = State()
    district = State()
    finish = State()

    next = State()
    previous = State()
    peoples = State()
    geopos = State()

    record = State()
    date = State()
    time_time = State()
    record_confirmation = State()


class Chat(StatesGroup):
    first = State()
    second = State()

    


