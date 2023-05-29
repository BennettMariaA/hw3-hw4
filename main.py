import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='6140983039:AAHLDQUE27uJES5kzgb52YsX8R9T5UQCulU')
dp = Dispatcher(bot, storage=MemoryStorage())

class MentorForm(StatesGroup):
    ID = State()
    NAME = State()
    DIRECTION = State()
    AGE = State()
    GROUP = State()

def create_mentors_table():
    conn = sqlite3.connect('mentors.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            direction TEXT,
            age INTEGER,
            group TEXT)
''')

    conn.commit()
    conn.close()


@dp.message_handler(Command('add_mentor'))
async def add_mentor_start(message: types.Message):
    await MentorForm.ID.set()
    await message.reply("Введите ID ментора:")

@dp.message_handler(state=MentorForm.ID)
async def process_mentor_id(message: types.Message, state: FSMContext):
    mentor_id = message.text

    await state.update_data(mentor_id=mentor_id)

    await MentorForm.NAME.set()
    await message.reply("Введите имя ментора:")

@dp.message_handler(state=MentorForm.NAME)
async def process_mentor_name(message: types.Message, state: FSMContext):
    mentor_name = message.text

    await state.update_data(mentor_name=mentor_name)

    await MentorForm.DIRECTION.set()
    await message.reply("Введите направление:")

@dp.message_handler(state=MentorForm.DIRECTION)
async def process_mentor_direction(message: types.Message, state: FSMContext):
    direction = message.text

    await state.update_data(direction=direction)

    await MentorForm.AGE.set()
    await message.reply("Введите возраст ментора:")

@dp.message_handler(state=MentorForm.AGE)
async def process_mentor_age(message: types.Message, state: FSMContext):
    age = message.text

    await state.update_data(age=age)

    await MentorForm.GROUP.set()
    await message.reply("Введите группу ментора:")

# Обработчик ввода группы ментора и завершение процесса создания ментора
@dp.message_handler(state=MentorForm.GROUP)
async def process_mentor_group(message: types.Message, state: FSMContext):
    group = message.text

    await state.update_data(group=group)

    mentor_data = await state.get_data()

    mentor_name = mentor_data['mentor_name']
    direction = mentor_data['direction']
    age = mentor_data['age']
    group = mentor_data['group']

    conn = sqlite3.connect('mentors.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO mentors (name, direction, age, group)
        VALUES (?, ?, ?, ?)
    ''', (mentor_name, direction, age, group))

    conn.commit()
    conn.close()

    await message.reply("Ментор добавлен в базу данных!")

if __name__ == '__main__':
    from aiogram import executor

executor.start_polling(dp, skip_updates=True)

