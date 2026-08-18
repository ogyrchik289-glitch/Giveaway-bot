from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_kb(participants: list):
    return InlineKeyboardMarkup(inline_keyboard=[
        InlineKeyboardButton(f"Присоедениться к розыгрышу✅ ({len(participants)})")
    ])
