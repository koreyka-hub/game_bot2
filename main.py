import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from config.config import TELEGRAM_TOKEN
from handlers.talk_handlers import talk_start, talk, say_contact
from handlers.start_handlers import start
from config.states import MAINMENU, TALK, GUESS_NUMBER
from handlers.guess_handlers import guess_number_start, guess_number
from random import randint


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
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
                CallbackQueryHandler(talk_start, pattern="talk"),
                CallbackQueryHandler(guess_number_start, pattern="guess_game"),
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            GUESS_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, guess_number),
                CallbackQueryHandler(guess_number, pattern="start_game"),
                CallbackQueryHandler(start, pattern="main_menu"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # & - и
    # | - или
    # ~ - не
    # Ты телеграм бот.Тебе отправляют название книги. Составь подробное, логично структурированное саммари с ключевыми идеями, концепциями, примерами и выводами. Сделай текст лёгким для восприятия — используй ассоциации, списки, шаги или метафоры. Итоговое саммари должно быть ясным, последовательным и полностью отражать содержание книги
    application.run_polling()
