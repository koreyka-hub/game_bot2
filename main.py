import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler
)
from dotenv import load_dotenv

import os

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

MAINMENU, TALK, BIBA = range(3)


# callback
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная информация о том, что произошло
    # update.effective_chat - вся инфа о чате
    # update.effective_user - вся инфа о пользователе
    # update.effective_message - вся инфа о сообщении
    # update.effective_message.text - текст сообщения
    keyboard = [
        [InlineKeyboardButton("Режим разговора", callback_data="talk")],
        [InlineKeyboardButton("Режим бибы", callback_data="biba")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {update.effective_user.first_name}!\n\nНапиши команду:\n /talk чтобы поговорить со мной.\n /biba чтобы получить бобу.",
        reply_markup=markup
    )
    return MAINMENU


async def biba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # query - запрос
    query = update.callback_query
    await query.answer()
    
    keyboard = [["биба"], ["боба"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="боба", reply_markup=markup
    )
    return BIBA


async def say_boba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["биба"],
        ["боба"],
        [KeyboardButton("поделиться контактом", request_contact=True)],
    ]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="боба", reply_markup=markup
    )


async def say_biba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="биба"
    )


async def say_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.effective_message.contact.phone_number
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Ваш номер: {phone_number}"
    )


async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы поговорить со мной, просто напиши любой текст.",
    )
    return TALK


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    if "привет" in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Здарово, брат!",
        )
    # чтобы тут обрабатывались 5 рандомных фраз
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    # handler - обработчик
    # CommandHandler - обработчик команд
    # MessageHandler - обработчик сообщений

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("talk", talk_start),
                CommandHandler("biba", biba),
                CallbackQueryHandler(biba, pattern="biba"),
                CallbackQueryHandler(talk_start, pattern="talk"),
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            BIBA: [
                MessageHandler(filters.Regex("^биба$"), say_boba),
                MessageHandler(filters.Regex("^боба$"), say_biba),
                MessageHandler(filters.CONTACT, say_contact),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # & - и
    # | - или
    # ~ - не

    application.run_polling()