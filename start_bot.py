import asyncio

from vkbottle.bot import Bot, BotLabeler

from base import create_tables
from chat import chat_labeler
from states import states_labeler
from callbacks import callback_labeler
from config import state_dispenser, COMMUNITY_TOKEN


def main():
    asyncio.run(create_tables())

    base_labeler = BotLabeler()
    labelers = [chat_labeler, states_labeler, callback_labeler, callback_labeler]
    for labeler in labelers:
        base_labeler.load(labeler)

    bot = Bot(token=COMMUNITY_TOKEN, labeler=base_labeler, state_dispenser=state_dispenser)
    asyncio.run(bot.run_polling())


if __name__ == '__main__':
    main()
