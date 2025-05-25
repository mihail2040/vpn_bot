import datetime

from aiogram import  F, Router, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery, LabeledPrice
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from l10n import __all__

import locale
locale.setlocale(locale.LC_ALL, '')
# 'ru_RU.utf8
import asyncio
import app.keyboards as kb
import app.database.requests as rq

router = Router()

class Add_key(StatesGroup):
    id_key = State()
    type_key = State()
    text_key = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_users(message.from_user.id)
    await message.answer('Привет, я бот для настройки ВПН',
                         reply_markup=kb.main)

@router.message(F.text == 'Настроить ВПН')
async def setting(message: Message):
    
    # await rq.set_users_mobile(message.from_user.id)
    # await message.answer(f'{callback.data}')
    
    
    user_profile = await rq.get_user_profile(message.from_user.id)
    if user_profile.sub_date_to >= datetime.datetime.now():
        await message.answer(
            f'У вас уже есть подписка до {user_profile.sub_date_to.strftime("%d %B %Y %H:%M:%S")}',
            reply_markup=kb.buy_tarif_second)
    else:
        # await callback.message.edit_text(f'Скачайте приложение Streisand из App Store.\nhttps://apps.apple.com/ru/app/streisand/id6450534064',disable_web_page_preview=True,
        #                           reply_markup=kb.download)
        await message.answer('Выберите услугу',
                                         reply_markup=kb.select_tarif)
    # await message.answer(text='Выберите свою ОС(телефон)',
    #                      reply_markup=kb.mobile)


@router.callback_query(F.data == 'backseltarif')
async def baclseltarif(callback: CallbackQuery):
    # await rq.set_users_mobile(callback.from_user.id, mobile)
    await callback.answer('')

    user_profile = await rq.get_user_profile(callback.from_user.id)
    if user_profile.sub_date_to >= datetime.datetime.now():
        await callback.message.edit_text(
            f'У вас уже есть подписка до {user_profile.sub_date_to.strftime("%d %B %Y %H:%M:%S")}',
                                                reply_markup=kb.buy_tarif_second)
    else:
        await callback.message.edit_text('Выберите услугу',
                                                reply_markup=kb.select_tarif)



@router.callback_query(F.data == 'backos')
async def backos(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text='Выберите свою ОС(телефон)',
                         reply_markup=kb.mobile)
    
@router.callback_query(F.data == 'os_ios')
@router.callback_query(F.data == 'os_android')
async def os_select(callback: CallbackQuery, bot: Bot): 
    # IOS = 1
    # Android = 2
    if callback.data == 'os_ios':
        mobile = 1
    elif callback.data == 'os_android':
        mobile = 2 
        
    await rq.set_users_mobile(callback.from_user.id, mobile)
    await callback.answer(f'{callback.data}')
    await guide_vpn(callback,bot)
    # user_profile = await rq.get_user_profile(callback.from_user.id)
    # if user_profile.sub_date_to >= datetime.datetime.now():
    #     await callback.message.edit_text(f'У вас уже есть подписка до {user_profile.sub_date_to.strftime("%d %B %Y %H:%M:%S")}',
    #                                      reply_markup=kb.buy_tarif_second)
    # else:
    #     # await callback.message.edit_text(f'Скачайте приложение Streisand из App Store.\nhttps://apps.apple.com/ru/app/streisand/id6450534064',disable_web_page_preview=True,
    #     #                           reply_markup=kb.download)
    #     await callback.message.edit_text('Выберите услугу',
    #                                      reply_markup=kb.select_tarif)


 
@router.callback_query(F.data == 'buyvpn')
async def android(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите тариф',
              reply_markup=kb.buy_tarif)

@router.callback_query(F.data == 'backmain')
async def ios(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.delete()

@router.callback_query(F.data == 'down')
async def download(callback: CallbackQuery,bot: Bot):
    await callback.answer('')
    user_profile = await rq.get_user_profile(callback.from_user.id)

    if user_profile:
        if user_profile.mobile == 1:
            await callback.message.edit_text('Через 10 секунд Вам придет ключ, нужно нажать на него, он скопируется.'
                                 '\nДалее зайдите в скачанное приложение Streisand и нажмите на плюс в правом верхнем углу,'
                                 '\nВыберите пункт "Вставить из буфера"'
                                 '\nРазрешите внести изменения и нажмите на кнопку включения расположенную в центре экрана.'
                                 '\nГотово'
                                 '\nДля отключение снова нажмите кнопку включения. ')

        if user_profile.mobile == 2:
            await callback.message.edit_text('Через 10 секунд Вам придет ключ, нужно нажать на него, он скопируется.'
                                         '\nДалее зайдите в скачанное приложение AmneziaVPN и нажмите на плюс в правом нижнем углу,'
                                         '\nВставьте текст в строку (можно нажать кноку "Вставить" справа"'
                                         '\nНажмите на появивщуюся кнопку "Продолжить"'
                                         '\nНажмите на появивщуюся кнопку "Подключиться"'
                                         '\nРазрешите внести изменения и нажмите на кнопку "Подключиться" расположенную в центре экрана.'
                                         '\nГотово'
                                         '\nДля отключение снова нажмите кнопку "Отключиться".')

        await asyncio.sleep(10)

        text_key = await rq.sel_key(callback.from_user.id)

        if text_key is None:
            await callback.message.answer('Извините, ключи закончились.\bПопробуйте через 10 минут')
            await bot.send_message(chat_id=392116437, text='ключи закончились')
        else:
            await callback.message.answer(f'Ваш ключ:\n`{text_key}`', parse_mode="MARKDOWN", reply_markup=kb.success)
            if callback.from_user.username:
                await bot.send_message(chat_id=392116437,
                                       text=f'Юзер @{callback.from_user.username} получил ключ')
            else:
                await bot.send_message(chat_id=392116437, text=f'Юзер @{callback.from_user.id} получил ключ')
    else:
        await callback.message.answer('Не указана ОС телефона')

@router.callback_query(F.data == 'backmobile')
async def ios(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите свою ОС(телефон)',
                                    reply_markup=kb.mobile)

@router.callback_query(F.data == 'freeweek')
async def freeweek(callback: CallbackQuery, bot: Bot):
    await callback.answer('')

    user_profile = await rq.get_user_profile(callback.from_user.id)

    if user_profile:
        if user_profile.freeweek == False:
            await callback.message.edit_text('Выберите свою ОС(телефон)',
                                             reply_markup=kb.mobile)
            # await guide_vpn(callback, bot)
            
            # if user_profile.mobile == 1:
            #     await callback.message.edit_text('Через 10 секунд Вам придет ключ, нужно нажать на него, он скопируется.'
            #                          '\nДалее зайдите в скачанное приложение Streisand и нажмите на плюс в правом верхнем углу,'
            #                          '\nВыберите пункт "Вставить из буфера"'
            #                          '\nРазрешите внести изменения и нажмите на кнопку включения расположенную в центре экрана.'
            #                          '\nГотово'
            #                          '\nДля отключение снова нажмите кнопку включения. ')
            # 
            # if user_profile.mobile == 2:
            #     await callback.message.edit_text('Через 10 секунд Вам придет ключ, нужно нажать на него, он скопируется.'
            #                                  '\nДалее зайдите в скачанное приложение AmneziaVPN и нажмите на плюс в правом нижнем углу,'
            #                                  '\nВставьте текст в строку (можно нажать кноку "Вставить" справа"'
            #                                  '\nНажмите на появивщуюся кнопку "Продолжить"'
            #                                  '\nНажмите на появивщуюся кнопку "Подключиться"'
            #                                  '\nРазрешите внести изменения и нажмите на кнопку "Подколючиться" расположенную в центре экрана.'
            #                                  '\nГотово'
            #                                  '\nДля отключение снова нажмите кнопку "Отключиться".')
            # 
            # await asyncio.sleep(10)
            # 
            # text_key = await rq.sel_key(callback.from_user.id)
            # 
            # if text_key is None:
            #     await callback.message.answer('Извините, ключи закончились.\bПопробуйте через 10 минут')
            #     await callback.message.send_copy(chat_id=392116437)
            # else:
            #     await callback.message.answer(f'Ваш ключ:\n`{text_key}`', parse_mode="MARKDOWN",reply_markup=kb.success)
        else:
            await callback.message.edit_text(f'Вы уже использовали тестовую неделю, теперь можете приобрести подписку',reply_markup=kb.buy_tarif)
    else:
        await callback.message.answer('Не создан профиль юзера, напишите администратору @mihail2040')

@router.callback_query(F.data == 'success')
async def download(callback: CallbackQuery, bot: Bot):
    await callback.answer('')
    await callback.message.delete()
    # await bot.delete_message(chat_id=callback.from_user.id,message_id=(callback.message.message_id - 1))
    
    await callback.message.answer('Не забывайте отключать впн, когда он не нужен'
                                  '\nвпн НЕ дает Вам анонимность'
                                  '\nНе скачивайте пиратский контент под ВПН и не совершайте противоправных действий')
    if callback.from_user.username:
        await bot.send_message(chat_id=392116437,text=f'Юзер @{callback.from_user.username} настроил ВПН')
    else:
        await bot.send_message(chat_id=392116437, text=f'Юзер @{callback.from_user.id} настроил ВПН')

@router.callback_query(F.data == 'buyvpn_100')
@router.callback_query(F.data == 'buyvpn_250')
async def buyvpn_(callback: CallbackQuery):

    if callback.data == 'buyvpn_100':
        amount = 70
        month = 1
    if callback.data == 'buyvpn_250':
        amount = 175
        month = 3
        
    await callback.answer('')
    await callback.message.answer_invoice(
        title="Оплата подписки",
        description= (f'Оплатить подписку на {month} месяц(а)'),
        prices=[LabeledPrice(label="XTR", amount=amount)],
        provider_token="",
        payload=(f'Заплатить {amount} звезд'),
        currency="XTR",
    )


@router.callback_query(F.data == 'guide_vpn')
async def guide_vpn(callback: CallbackQuery, bot: Bot):
    await callback.answer('')

    user_profile = await rq.get_user_profile(callback.from_user.id)

    if user_profile: 
            if user_profile.mobile == 1:
                await callback.message.edit_text(f'Скачайте приложение Streisand из App Store.\nhttps://apps.apple.com/ru/app/streisand/id6450534064',disable_web_page_preview=True,
                                          reply_markup=kb.download)
                # await callback.message.edit_text('Через 10 секунд Вам придет ключ, нужно нажать на него, он скопируется.'
                #                      '\nДалее зайдите в скачанное приложение Streisand и нажмите на плюс в правом верхнем углу,'
                #                      '\nВыберите пункт "Вставить из буфера"'
                #                      '\nРазрешите внести изменения и нажмите на кнопку включения расположенную в центре экрана.'
                #                      '\nГотово'
                #                      '\nДля отключение снова нажмите кнопку включения. ')

            if user_profile.mobile == 2:
                await callback.message.edit_text(f'Скачайте приложение Amneziavpn из Play Market.\nhttps://play.google.com/store/apps/details?id=org.amnezia.vpn',disable_web_page_preview=True,
                                          reply_markup=kb.download)
                # await callback.message.edit_text('Через 10 секунд Вам придет ключ, нужно нажать на него, он скопируется.'
                #                              '\nДалее зайдите в скачанное приложение AmneziaVPN и нажмите на плюс в правом нижнем углу,'
                #                              '\nВставьте текст в строку (можно нажать кноку "Вставить" справа"'
                #                              '\nНажмите на появивщуюся кнопку "Продолжить"'
                #                              '\nНажмите на появивщуюся кнопку "Подключиться"'
                #                              '\nРазрешите внести изменения и нажмите на кнопку "Подколючиться" расположенную в центре экрана.'
                #                              '\nГотово'
                #                              '\nДля отключение снова нажмите кнопку "Отключиться".')

            # await asyncio.sleep(10)
            #
            # text_key = await rq.sel_key(callback.from_user.id)
            #
            # if text_key is None:
            #     await callback.message.answer('Извините, ключи закончились.\bПопробуйте через 10 минут')
            #     await bot.send_message(chat_id=392116437,text='ключи закончились')
            # else:
            #     await callback.message.answer(f'Ваш ключ:\n`{text_key}`', parse_mode="MARKDOWN",reply_markup=kb.success)
            #     if callback.from_user.username:
            #         await bot.send_message(chat_id=392116437,
            #                                text=f'Юзер {callback.from_user.username} получил ключ')
            #     else:
            #         await bot.send_message(chat_id=392116437, text=f'Юзер {callback.from_user.id} получил ключ')
    else:
        await callback.message.answer('Не указана ОС телефона, напишите в поддержку @mihail2040')
        
 
@router.message(F.text == 'Помощь')
async def help(message: Message):
    await message.answer('Выберите проблему:',reply_markup=kb.help)


@router.callback_query(F.data == 'exit')
async def exit(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.delete()

@router.callback_query(F.data == 'problem_work')
async def problem_work(callback: CallbackQuery):
    await callback.answer('')
 
    await callback.message.edit_text('Напишите о проблеме администратору @mihail2040')
    
@router.callback_query(F.data == 'problem_guide')
async def problem_guide(callback: CallbackQuery):
    await callback.answer('')

    await callback.message.edit_text('Напишите о проблеме администратору @mihail2040')
    
@router.callback_query(F.data == 'problem_all')
async def problem_all(callback: CallbackQuery):
    await callback.answer('')

    await callback.message.edit_text('Напишите о проблеме администратору @mihail2040')

@router.message(F.text == 'Статус подписки')
async def status_tarif(message: Message):

    user_profile = await rq.get_user_profile(message.from_user.id)
    if user_profile.sub_date_to >= datetime.datetime.now():
        await message.answer(f'У вас уже есть подписка до {user_profile.sub_date_to.strftime("%d %B %Y %H:%M:%S")}')
    else:
        await message.answer('У вас нет активной подписки')

@router.message(F.text == 'Продлить подписку')
async def prolong_tarif(message: Message):

    user_profile = await rq.get_user_profile(message.from_user.id)
    if user_profile.sub_date_to >= datetime.datetime.now():
        await message.answer(f'У вас уже есть подписка до {user_profile.sub_date_to.strftime("%d %B %Y %H:%M:%S")}',reply_markup=kb.prolong_tarif)
    else:
        await message.answer('У вас нет активной подписки',reply_markup=kb.prolong_tarif)
        

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def success_payment_handler(message: Message):
    amount = message.successful_payment.total_amount
    charge_id = message.successful_payment.telegram_payment_charge_id
    date = await rq.user_buy_vpn(message.from_user.id,charge_id,amount)
    await message.answer(f'Оплата прошла успешно:\nВаша подписка активна до {date.strftime("%d %B %Y %H:%M:%S")}')

@router.message(Command('admin'))
async def cmd_start(message: Message):
    await rq.set_users(message.from_user.id)
    
    if message.from_user.id == 392116437:
        await message.answer('Меню админа',reply_markup=kb.admin)
        
        
@router.callback_query(F.data == 'count_key')
async def count_key(callback: CallbackQuery):
    await callback.answer('')
    key_ios, key_andriod = await rq.key_count()
    await callback.message.answer(f'Ios ключей = {key_ios}'
                         f'\nAndroid ключей = {key_andriod}',reply_markup=kb.do_it)
    # reply_markup=kb.main)

@router.callback_query(F.data == 'delete_key')
async def delete_key(callback: CallbackQuery):
    await callback.answer('')
    keys = await rq.key_for_delete()
    await callback.message.answer(f'Ключи на удаление:{','.join(str(x) for x in keys)}',reply_markup=kb.do_it)



#State
@router.callback_query(F.data == 'add_key')
async def add_key(callback: CallbackQuery,state: FSMContext ):
    await callback.answer('')
    last_id = await rq.last_key_id()
    await state.set_state(Add_key.id_key)
    await callback.message.answer(f'Последний ключ с номером {last_id}'
                                  f'\nВведи новый id_key',reply_markup=kb.exit_state)
    
@router.message(Add_key.id_key)
async def add_key_1(message: Message, state: FSMContext):
    if int(message.text) > await rq.last_key_id():
        await state.update_data(id_key=message.text)
        await state.set_state(Add_key.type_key)
        key_type = await rq.all_key_type()
        await message.answer(f'Введи тип ключа'
                             f'\n{"\n".join([" - ".join(str(row.type_key) for row in key_type )])}',reply_markup=kb.exit_state)
    else:
        await message.answer('Ti ebobo?',reply_markup=kb.exit_state)

@router.message(Add_key.type_key)
async def add_key_1(message: Message, state: FSMContext):
    key_type = []
    for type_key in await rq.all_key_type():
        key_type.append(type_key.type_key)
    if int(message.text) in key_type:
        await state.update_data(type_key=message.text)
        await state.set_state(Add_key.text_key)
        await message.answer('Введи сам ключ',reply_markup=kb.exit_state)
    else:
        await message.answer('Нет такого?',reply_markup=kb.exit_state)


@router.message(Add_key.text_key)
async def add_key_1(message: Message, state: FSMContext):
        await state.update_data(text_key=message.text)
        new_key = await state.get_data()
        await rq.add_key(new_key)
        await state.clear()
        await message.answer('Ключ добавлен')
     
@router.callback_query(F.data == 'exit_state')
async def exit(callback: CallbackQuery,state: FSMContext):
    await callback.answer('')
    await callback.message.delete()
    await state.clear()

