import datetime
import sqlite3

from datetime import timedelta
from calendar import monthrange
from app.database.models import async_session
from app.database.models import User, Key, Key_User, User_profile, Payments,Type_key
from sqlalchemy import select, update, delete, exc, func, join,DateTime
from dateutil.relativedelta import relativedelta

async def set_users(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))            

        user_profile = await session.scalar(select(User_profile).where(User_profile.id_user == user.id_user))
        if not user_profile:
            session.add(User_profile(id_user=user.id_user,sub_date_from=datetime.date(2000, 1, 1),
                                     sub_date_to=datetime.date(2000, 1, 1),mobile=0))

        await session.commit()

async def set_users_mobile(tg_id,mobile):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user_profile = await session.scalar(select(User_profile).where(User_profile.id_user == user.id_user))
            if user_profile:
                user_profile.mobile = mobile
            else:
                session.add(User_profile(id_user=user.id_user,mobile=mobile,sub_date_from=datetime.date(2000,1,1),sub_date_to=datetime.date(2000,1,1)))

            await session.commit()

async def sel_key(tg_id):
    async with async_session() as session:
        
        id_user = await session.scalar(select(User.id_user).where(User.tg_id == tg_id))
        if  id_user:
            
            user_profile = await session.scalar(select(User_profile).where(User_profile.id_user == id_user))
            if user_profile:
                
                if user_profile.freeweek == False and user_profile.sub_date_from.date() < datetime.date(2001,1,1,):
                    
                    user_profile.freeweek = True
                    user_profile.sub_date_from = datetime.datetime.now()
                    user_profile.sub_date_to = datetime.datetime.now() + datetime.timedelta(7)

                    id_key = await session.scalar(select(Key_User.id_key).where(Key_User.id_user == id_user and Key_User.type_key == user_profile.mobile))
                    if not id_key:
                        key = await session.scalar(select(Key).where(Key.type_key == user_profile.mobile and Key.used == False))
                        session.add(Key_User(id_key=key.id_key, id_user=id_user, type_key=user_profile.mobile))
                        key.used = True
                        text_key = key.text_key
                        try:
                            await session.commit()
                        except exc.IntegrityError:
                            return None
                        return text_key
                    else:
                        key = await session.scalar(select(Key).where(Key.id_key == id_key))
                        text_key = key.text_key
                        try:
                            await session.commit()
                        except exc.IntegrityError:
                            return None
                        return text_key
                    
                elif user_profile.sub_date_to > datetime.datetime.now():
                    
                        id_key = await session.scalar(select(Key_User.id_key).where(Key_User.id_user == id_user and Key_User.type_key == user_profile.mobile))
                        if not id_key:
                            key = await session.scalar(select(Key).where(Key.type_key == user_profile.mobile and Key.used == False))
                            session.add(Key_User(id_key=key.id_key,id_user=id_user,type_key=user_profile.mobile))
                            key.used = True
                            text_key = key.text_key
                            try:
                                await session.commit()
                            except exc.IntegrityError:
                                return None
                            return text_key
                        else:
                            key = await session.scalar(select(Key).where(Key.id_key == id_key))
                            text_key = key.text_key
                            return text_key
          
                else:
                    return None
            else:
                return None
        else:
            return None       

async def user_buy_vpn(tg_id,telegram_payment_charge_id,amount):
    async with async_session() as session:

        id_user = await session.scalar(select(User.id_user).where(User.tg_id == tg_id))

        session.add(Payments(id_user=id_user,telegram_payment_charge_id=telegram_payment_charge_id,date_payments=datetime.datetime.now(),total_amount=amount,refund=False))

        user_profile = await session.scalar(select(User_profile).where(User_profile.id_user == id_user))

        # current_year = datetime.now().year
        # month = datetime.now().month  # int(input())
        if amount == 70:
            month = 1
        if amount == 175:
            month = 3
        if user_profile.sub_date_to < datetime.datetime.now():
            user_profile.sub_date_from = datetime.datetime.now()
            user_profile.sub_date_to = datetime.datetime.now() + relativedelta(months=+month)
        else:
            user_profile.sub_date_to = user_profile.sub_date_to + relativedelta(months=+month)

        date_to = user_profile.sub_date_to
        await session.commit()
        return date_to

async def get_user_profile(tg_id):
    async with async_session() as session:
        id_user = await session.scalar(select(User.id_user).where(User.tg_id == tg_id))
        user_profile = await session.scalar(select(User_profile).where(User_profile.id_user == id_user))
        # user_profile = await session.scalar(select(User_profile).where(User_profile.id_user == select(User.id_user).where(User.tg_id == tg_id)))
        return user_profile
    
async def key_count():
    async with async_session() as session:
        key_ios = await session.scalar(
            select(func.count()).select_from(Key).where(Key.type_key == 1 and Key.used == False))
        key_android = await session.scalar(
            select(func.count()).select_from(Key).where(Key.type_key == 2 and Key.used == False))
        return key_ios,key_android


async def key_for_delete():
    async with async_session() as session:
        return await session.scalars(select(Key.id_key).where(Key.need_deactivate == True))
        # return await session.scalars(select(Key.id_key).where(Key.used == True))
    
async def last_key_id():
    async with async_session() as session:
        return await session.scalar(select(func.max(Key.id_key)))

async def all_key_type():
    async with async_session() as session:
        # key_type = await session.scalars(select(Type_key)) 
        # return key_type
        return await session.scalars(select(Type_key).where(Type_key.type_key is not None))

async def add_key(new_key):#id_key,type_key,text_key):
    async with async_session() as session:
        session.add(Key(id_key=new_key["id_key"],type_key=new_key["type_key"],text_key=new_key["text_key"]))
        await session.commit()

async def check_user_tarif():
    async with async_session() as session:
        date_2 = datetime.datetime.now() + timedelta(days=2)
        user_profile = await session.scalars(select(User_profile).where(User_profile.sub_date_to.between(datetime.datetime.now(), date_2)))
        spisok2 = []
        
        format = '%d %B %Y %H:%M:%S'
        for row in user_profile:
            # tg_id = await session.scalar(select(User.tg_id).where(User.id_user == row.id_user))
            spisok = []
            spisok.append(await session.scalar(select(User.tg_id).where(User.id_user == row.id_user)))
            spisok.append(row.sub_date_to.strftime(format))
            # spisok.append(row.sub_date_to)
            spisok2.append(spisok)
            
        # return await session.scalars(select(User_profile.id_user).where(User_profile.sub_date_to.between(datetime.datetime.now(),date_2)))
        return spisok2