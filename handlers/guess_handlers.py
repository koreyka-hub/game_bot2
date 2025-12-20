from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import ContextTypes
from config.states import GUESS_NUMBER


async def guess_number_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("Угадать число", callback_data="start_game")]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Давай сыграем в игру! Я попробую угадать загаданное тобой число от 1 до 100. Нажми кнопку ниже, когда будешь готов!",
        reply_markup=markup,
    )
    context.user_data["start"] = 1
    context.user_data["end"] = 100
    context.user_data["mid"] = 50
    
    return GUESS_NUMBER


async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["больше"], ["меньше"], ["угадал"]]
    markup = ReplyKeyboardMarkup(keyboard)
    query = update.callback_query
    if query:
        await query.answer()
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="50?", reply_markup=markup
        )
    else:
        text = update.effective_message.text
        if text == "больше":
            context.user_data["start"] = context.user_data["mid"]
            context.user_data["mid"] = (
                context.user_data["start"] + context.user_data["end"]
            ) // 2
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{context.user_data['mid']}?",
                reply_markup=markup,
            )
        elif text == "меньше":
            context.user_data["end"] = context.user_data["mid"]
            context.user_data["mid"] = (
                context.user_data["start"] + context.user_data["end"]
            ) // 2
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{context.user_data['mid']}?",
                reply_markup=markup,
            )
        elif text == "угадал":
            keyboard = [
                [InlineKeyboardButton("вернуться в меню", callback_data="main_menu")],
                [InlineKeyboardButton("новая игра", callback_data="start_game")],
            ]
            markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ура! Я угадал твоё число!",
                reply_markup=markup,
            )
    return GUESS_NUMBER
