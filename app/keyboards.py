from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Настроить ВПН'),KeyboardButton(text='Статус подписки')],
    [KeyboardButton(text='Продлить подписку'), KeyboardButton(text='Помощь')]
],
    resize_keyboard=True,
    # one_time_keyboard=True,
    input_field_placeholder='Выберите пункт меню')

mobile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='IOS(IPhone)',callback_data='os_ios'),InlineKeyboardButton(text='Android',callback_data='os_android')],
    [InlineKeyboardButton(text='Назад',callback_data='backseltarif')]
])

download = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Скачал',callback_data='down')],
    [InlineKeyboardButton(text='Назад',callback_data='backmobile')]
])

select_tarif = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Тестовая неделя',callback_data='freeweek')],
    [InlineKeyboardButton(text='Купить подписку',callback_data='buyvpn')],
    [InlineKeyboardButton(text='Назад',callback_data='exit')]
])

success = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='У меня получилось',callback_data='success')],
])

buy_tarif = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить подписку на месяц (70 ⭐)',callback_data='buyvpn_100')],
    [InlineKeyboardButton(text='Купить подписку на 3 месяца (175 ⭐)',callback_data='buyvpn_250')],
    [InlineKeyboardButton(text='Назад',callback_data='backseltarif')]
])

buy_tarif_second = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Настроить ВПН заново',callback_data='backos')],
    [InlineKeyboardButton(text='Купить подписку на месяц (70 ⭐)',callback_data='buyvpn_100')],
    [InlineKeyboardButton(text='Купить подписку на 3 месяца (175 ⭐)',callback_data='buyvpn_250')],
    [InlineKeyboardButton(text='Назад',callback_data='backos')]
])

help = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Не работает ВПН',callback_data='problem_work')],
    [InlineKeyboardButton(text='Не могу настроить ВПН',callback_data='problem_guide')],
    [InlineKeyboardButton(text='Другая проблема',callback_data='problem_all')],
    [InlineKeyboardButton(text='Закрыть',callback_data='exit')]
])

prolong_tarif = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить подписку на месяц (70 ⭐)',callback_data='buyvpn_100')],
    [InlineKeyboardButton(text='Купить подписку на 3 месяца (175 ⭐)',callback_data='buyvpn_250')],
    [InlineKeyboardButton(text='Закрыть',callback_data='exit')]
])


admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кол-во ключей',callback_data='count_key')],
    [InlineKeyboardButton(text='Добавить ключи',callback_data='add_key')],
    [InlineKeyboardButton(text='Ключи на удаление',callback_data='delete_key')],
    [InlineKeyboardButton(text='Закрыть',callback_data='exit')]
])

do_it = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сделал',callback_data='exit')]])

exit_state = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выйти',callback_data='exit_state')]])