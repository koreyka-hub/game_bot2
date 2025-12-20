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
        [InlineKeyboardButton("Режим разговора", callback_data="talk")],
        [InlineKeyboardButton("Режим игры", callback_data="guess_game")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {update.effective_user.first_name}!\n\nНапиши команду:\n /talk чтобы поговорить со мной.\n /guess_game чтобы поиграть.",
        reply_markup=markup,
    )
    return MAINMENU
