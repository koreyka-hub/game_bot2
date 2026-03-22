from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes,ConversationHandler
from config.states import MAINMENU,GET_AGE
from db.user_crud import add_user, get_user, update_age

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная информация о том, что произошло
    # update.effective_chat - вся инфа о чате
    # update.effective_user - вся инфа о пользователе
    # update.effective_message - вся инфа о сообщении
    # update.effective_message.text - текст сообщения
    user = await get_user(update.effective_user.id)
    #print(user['id'], user['tg_id'], user['name'])
    if not user:
        user = await add_user(update.effective_user.id)
    if not user["age"]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Привет! Сколько тебе лет?"
        )
        return GET_AGE
    if user["age"] > 30:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Атстань, Скуф!"
        )
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("разговор", callback_data="talk")],
        [InlineKeyboardButton("угадай число", callback_data="guess_game")],
        [InlineKeyboardButton("крестики нолики", callback_data="tictactoe")],
        [InlineKeyboardButton("крестики нолики с игроками", callback_data="online_tictactoe")],
        [InlineKeyboardButton("крестики нолики с ботом", callback_data="bot_tictactoe")],

    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {update.effective_user.first_name}!\n как могу помочь?",
        reply_markup=markup,
    )
    return MAINMENU

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = update.effective_message.text
    # написать здесь проверку на дурака
    if not age.isdigit():
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Введи число."
        )
        return GET_AGE
    age = int(age)
    user = await update_age(update.effective_user.id, age)
    return await start(update, context)
