import os

from vkbottle import API, BuiltinStateDispenser


COMMUNITY_TOKEN = os.getenv('COMMUNITY_TOKEN', None)
USER_TOKEN = os.getenv('USER_TOKEN', None)


state_dispenser = BuiltinStateDispenser()
api = API(USER_TOKEN)
