from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback


search_keyboard = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Поиск'))
    .get_json()
)


def get_pagination_keyboard(user_id, last, liked):
    button_like = Callback('Like', payload={'cmd': 'like', 'user_id': user_id})
    button_next = Callback('Next', payload={'cmd': 'next', 'user_id': user_id})
    button_open_link = Callback('Посмотреть', payload={'cmd': 'open_link', 'link': f'https://vk.com/id{user_id}'})

    pagination_keyboard = Keyboard(one_time=False, inline=True)
    if not liked:
        pagination_keyboard.add(button_like, color=KeyboardButtonColor.NEGATIVE)
        if not last:
            pagination_keyboard.add(button_next, color=KeyboardButtonColor.PRIMARY)
        pagination_keyboard.row()
    pagination_keyboard.add(button_open_link)
    return pagination_keyboard.get_json()
