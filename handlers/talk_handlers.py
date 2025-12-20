from openai import OpenAI
client = OpenAI()


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
        if len(context.user_data["previous_messages"]) > 6:
            context.user_data["previous_messages"].pop(0)
            context.user_data["previous_messages"].pop(0)
        client = OpenAI()
        response = client.responses.create(
            model="gpt-5-mini",
            reasoning={"effort": "medium"},
            input=[
                {
                    "role": "developer",
                    "content": 'Тебе отправляют название книги.Максимум 4000 символов.Составь подробный,логично структурированное саммари с ключевыми идеями, концепциями, примерами и выводами. Сделай текст лёгким для восприятия — используй ассоциации, списки, шаги или метафоры. Итоговое саммари должно быть ясным, последовательным и полностью отражать содержание книги',
                },
            ]
            + context.user_data["previous_messages"]
            + [
                {
                    "role": "user",
                    "content": text,
                }
            ],
        )
        response_text = response.output_text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text,
        )
        context.user_data["previous_messages"].append(
            {"role": "user", "content": text}
        )
        context.user_data["previous_messages"].append(
            {"role": "assistant", "content": response_text}
        )
    

async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    previous_messages = []
    context.user_data["previous_messages"] = previous_messages
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Давай поговорим! Напиши мне что-нибудь."
    )
    return TALK

async def say_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.effective_message.contact.phone_number
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Ваш номер: {phone_number}"
    )