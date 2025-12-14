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
from config.config import TELEGRAM_TOKEN
from handlers.biba_handlers import biba, say_boba, say_biba
from handlers.talk_handlers import talk_start, talk, say_contact
from handlers.start_handlers import start
from config.states import MAINMENU, TALK, BIBA, GAME, GUESS_NUMBER
import random
from random import randint



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

MAINMENU, TALK, BIBA, GAME, GUESS_NUMBER = range(5)


# callback
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная информация о том, что произошло
    # update.effective_chat - вся инфа о чате
    # update.effective_user - вся инфа о пользователе
    # update.effective_message - вся инфа о сообщении
    # update.effective_message.text - текст сообщения
    keyboard = [
        [InlineKeyboardButton("Режим разговора", callback_data="talk")],
        [InlineKeyboardButton("Режим игры", callback_data="game_start")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {update.effective_user.first_name}!\n\nНапиши команду:\n /talk чтобы поговорить со мной.\n /game_start или /guess_game чтобы поиграть.",
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
        text="Чтобы поговорить со мной, просто напиши любой текст."
    )
    return TALK

async def game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chisl = random.randint(1,99)
    guess_chisl = int(input("я загадал число от 1 до 99,попробуй его угадать!"))
    if guess_chisl == chisl:
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="ты угадал,молодец!")
    elif guess_chisl.isdigit == False :
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="напиши число пожалуйста")
    else:
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="хорошая попытка,попробуй еще раз!")

    return GAME 

async def guess_number_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="привет,в этой игре тебе надо будет загадать число,а я буду его угадывать.Только честно!")
    keyboard = [["больше"], ["меньше"], ["угадал"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="50?",
        reply_markup=markup
    )
    return GUESS_NUMBER

async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    
    return GUESS_NUMBER


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
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )
    return TALK


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
                CommandHandler("guess_game", guess_number_start),
                CommandHandler("game", game_start)
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            BIBA: [
                MessageHandler(filters.Regex("^биба$"), say_boba),
                MessageHandler(filters.Regex("^боба$"), say_biba),
                MessageHandler(filters.CONTACT, say_contact),
            ],
            GAME:[],
            GUESS_NUMBER:[]
        },
        fallbacks=[CommandHandler("start", start)]
    )   

    application.add_handler(conv_handler)

    # & - и
    # | - или
    # ~ - не
    # Ты телеграм бот.Тебе отправляют название книги. Составь подробное, логично структурированное саммари с ключевыми идеями, концепциями, примерами и выводами. Сделай текст лёгким для восприятия — используй ассоциации, списки, шаги или метафоры. Итоговое саммари должно быть ясным, последовательным и полностью отражать содержание книги
    application.run_polling()