from aiogram import Router, Bot
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext  
from aiogram.filters import StateFilter
from keyboard import build_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models import Gieveaway
import asyncio
from aiogram.utils.markdown import hbold
from html import escape

handler_router = Router()


giveaway: Gieveaway | None = None

@handler_router.message(F.text.startswith("/start_giveaway"))
async def start_giveaway(message: Message, bot: Bot):
    global giveaway
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Пожалуйста введите название розыгрыша: /giveaway название розыгрыша")
        return
    else:
        text = escape(parts[1])
    data = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if data.status in ("creator", "administrator"):
        sent = await message.answer(f"""Внимание начинается розыгрыш❗️
Розыгрывается: {text}
Для участия нажмите на кнопку ниже⬇️

Итоги через 25 минут!""", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=f"Присоединиться к розыгрышу✅", callback_data="add_p")
    ]]))
        giveaway = Gieveaway(sent.chat.id, sent.message_id, text)
        giveaway.task = asyncio.create_task(finish_giveaway(giveaway, bot, 1500))    
    else:
        await message.answer("У вас нет прав на эту команду🚫")
            
@handler_router.callback_query(F.data == "add_p")
async def on_join(callback: CallbackQuery):
    if giveaway is None or not giveaway.is_active:
        await callback.answer("На данный момент нет активного розыгрыша🔴")
        return
    else:
            
        if giveaway.add_participant(callback.from_user.id):
            await callback.answer("Ты учавствуешь в розыгрыше🟢")
            await callback.message.edit_reply_markup(reply_markup=build_kb(giveaway.participants))
        else:
            await callback.answer("Ты уже принимаешь участие🔴")
            
async def finish_giveaway(giveaway: Gieveaway, bot: Bot, delay: int | None = None):
    if delay is not None:
        await asyncio.sleep(delay)
        
    else:
        giveaway.task.cancel()
    if not giveaway.participants:
            await bot.edit_message_text(text="""Розыгрыш завершен❗️
        Так как никто из участников группы не принял участие, победителей нет🔴""", chat_id=giveaway.chat_id, message_id=giveaway.message_id, reply_markup=None)
            giveaway.is_active = False
            return
    winners = giveaway.draw_winner()
    if len(winners) == 3:
        winner_text = f"""Розыгрыш завершен❗️
Первое место 🥇: <a href='tg://user?id={winners[0]}'>участник</a>🏆
Второе место 🥈: <a href='tg://user?id={winners[1]}'>участник</a>🏆
Третье место 🥉: <a href='tg://user?id={winners[2]}'>участник</a>🏆
Поздравляем🎉"""
    
    elif len(winners) == 2:
        winner_text = f"""Розыгрыш завершен❗️
Первое место 🥇: <a href='tg://user?id={winners[0]}'>участник</a>🏆
Второе место 🥈: <a href='tg://user?id={winners[1]}'>участник</a>🏆
Поздравляем🎉"""
    else:
        winner_text = f"""Розыгрыш завершен❗️
Первое место 🥇: <a href='tg://user?id={winners[0]}'>участник</a>🏆
Поздравляем🎉"""
    await bot.edit_message_text(text=winner_text, chat_id=giveaway.chat_id, message_id=giveaway.message_id, reply_markup=None)
        
@handler_router.message(Command("draw"))
async def draw(message: Message, bot: Bot):
    data = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if data.status in ("creator", "administrator"):
        if giveaway is None or not giveaway.is_active:
            await message.answer("Сейчас нет активного розыгрыша🔴")
            return
        await finish_giveaway(giveaway, bot)
    else:
        await message.answer("У вас нет прав на эту команду🚫")
        return