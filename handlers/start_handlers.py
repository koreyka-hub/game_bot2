from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import ContextTypes
from config.states import MAINMENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная информация о том, что произошло
    # update.effective_chat - вся инфа о чате
    # update.effective_user - вся инфа о пользователе
    # update.effective_message - вся инфа о сообщении
    # update.effective_message.text - текст сообщения
    keyboard = [
        [InlineKeyboardButton("разговор", callback_data="talk")],
        [InlineKeyboardButton("угадай число", callback_data="guess_game")],
        [InlineKeyboardButton("крестики нолики", callback_data="tictactoe")],
        [InlineKeyboardButton("крестики нолики с игроками", callback_data="tictactoe_online")],
        [InlineKeyboardButton("крестики нолики с ботом", callback_data="tictactoe_bot")],

    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {update.effective_user.first_name}!\n\n хочешь поговорить со мной,\n или поиграть в игры?",
        reply_markup=markup,
    )
    return MAINMENU
