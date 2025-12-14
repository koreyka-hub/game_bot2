from openai import OpenAI


from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes
)
from config.states import TALK

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    if "привет" in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Здарово, брат!",
        )
    elif "как дела?" in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Лучше всех!",
        )
    elif "какой твой любимый цвет?" in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Синий",
        )
    elif "пока" in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Пока, не пропадай!",
        )
    elif "как тебя зовут?" in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Меня зовут Гейм-Бот.",
        )
    elif "что ты умеешь?" in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Я могу с тобой поговорить и отправить бобу!",
        )
    # чтобы тут обрабатывались 5 рандомных фраз
    else:
        
    return TALK

async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы поговорить со мной, просто напиши любой текст."
    )
    return TALK

async def say_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.effective_message.contact.phone_number
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Ваш номер: {phone_number}"
    )