from aiogram import  Bot

import app.database.requests as rq
import app.keyboards as kb

async def key_free_count(bot: Bot):

    key_ios,key_android = await rq.key_count()
    if key_ios < 5:
        await bot.send_message(chat_id=392116437, text=f'Ключей под IOS(ZRAY) = {key_ios}')
         
    if key_android < 5:
        await bot.send_message(chat_id=392116437, text=f'Ключей под Android(amnezia) = {key_android}')
        
async def check_user_tarif(bot: Bot):
        user_profile = await rq.check_user_tarif()
        for id in user_profile:
            await bot.send_message(chat_id=id[0], text=f'У вас скоро кончается подписка:  {id[1]}',reply_markup=kb.prolong_tarif)
            await asyncio.sleep(3)
        