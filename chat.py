from vkbottle.bot import BotLabeler
from vkbottle.bot import Message

from config import api
from messages import hi, find
from states import check_user
from keyboards import search_keyboard


chat_labeler = BotLabeler()


@chat_labeler.private_message(text=['Начать', 'начать'])
async def start(message: Message):
    users = await api.users.get(message.from_id)
    await message.answer(hi.format(users[0].first_name), keyboard=search_keyboard)


@chat_labeler.private_message(text=['Поиск'])
async def search(message: Message):
    await message.answer(find)
    await check_user(message)
