from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ContextTypes
)
from config.states import BIBA

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
