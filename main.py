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
from handlers.talk_handlers import talk_start, talk
from handlers.start_handlers import start
from config.states import MAINMENU, TALK, GUESS_NUMBER, TICTACTOE, TICTACTOE_ONLINE, TICTACTOE_BOT
from handlers.guess_handlers import guess_number_start, guess_number
from handlers.tictactoe_handlers import tictactoe,tictactoe_start
from handlers.ttt_online import tictactoe_online_start
from handlers.ttt_bot import tictactoe_bot_start,tictactoe_bot
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
                CallbackQueryHandler(start, pattern="main_menu"),
                CallbackQueryHandler(talk_start, pattern="talk"),
                CallbackQueryHandler(guess_number_start, pattern="guess_game"),
                CallbackQueryHandler(tictactoe_start, pattern="tictactoe"),
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            GUESS_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, guess_number),
                CallbackQueryHandler(guess_number, pattern="start_game"),
                CallbackQueryHandler(start, pattern="main_menu"),],
            TICTACTOE:  [
            CallbackQueryHandler(tictactoe, pattern="^[0-8]$")
            ],
            TICTACTOE_ONLINE: [
                CallbackQueryHandler(
                    tictactoe_online_start, pattern="tictactoe_online"
                ),
                CallbackQueryHandler(tictactoe_online_start, pattern="^[0-8]$")
            ],
            TICTACTOE_BOT: [CallbackQueryHandler(tictactoe_bot_start, pattern = "tictactoe_bot"),
                            CallbackQueryHandler(tictactoe_bot, pattern="^[0-8]$")]
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # & - и
    # | - или
    # ~ - не
    # Ты телеграм бот.Тебе отправляют название книги. Составь подробное, логично структурированное саммари с ключевыми идеями, концепциями, примерами и выводами. Сделай текст лёгким для восприятия — используй ассоциации, списки, шаги или метафоры. Итоговое саммари должно быть ясным, последовательным и полностью отражать содержание книги
    application.run_polling()
