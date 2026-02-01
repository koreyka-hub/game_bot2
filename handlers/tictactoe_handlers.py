from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.states import TICTACTOE,MAINMENU


async def tictactoe_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query  # Полная информация о нажатой кнопке
    await query.answer()  # отвечаем на запрос
    context.user_data["i"] = "❌"
    context.user_data["h"] = 0
    context.user_data["lst"] = [
        "⬜",
        "⬜",
        "⬜",
        "⬜",
        "⬜",
        "⬜",
        "⬜",
        "⬜",
        "⬜",
    ]
    lst = context.user_data["lst"]  # Получаем список из user_data
    keyboard = [
        [
            InlineKeyboardButton(lst[0], callback_data="0"),
            InlineKeyboardButton(lst[1], callback_data="1"),
            InlineKeyboardButton(lst[2], callback_data="2"),
        ],
        [
            InlineKeyboardButton(lst[3], callback_data="3"),
            InlineKeyboardButton(lst[4], callback_data="4"),
            InlineKeyboardButton(lst[5], callback_data="5"),
        ],
        [
            InlineKeyboardButton(lst[6], callback_data="6"),
            InlineKeyboardButton(lst[7], callback_data="7"),
            InlineKeyboardButton(lst[8], callback_data="8"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Игра Крестики-нолики. Ты играешь за крестики, я за нолики. Нажми на кнопку, чтобы начать игру.",
        reply_markup=markup,
    )
    return TICTACTOE


async def tictactoe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    i = context.user_data["i"]
    nomer_knopki = int(query.data)
    lst = context.user_data["lst"]
    if lst[nomer_knopki] == "⬜":
        lst[nomer_knopki] = i
        if i == "❌":
            context.user_data["i"] = "⭕️"
        else:
            context.user_data["i"] = "❌"
        context.user_data["h"] += 1
        # победа
        keyboard = [
            [InlineKeyboardButton("играть заново", callback_data="tictactoe")],
            [InlineKeyboardButton("выйти в меню", callback_data="main_menu")],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        if lst[0] == lst[3] == lst[6] and lst[0] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif lst[0] == lst[1] == lst[2] and lst[1] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif lst[2] == lst[5] == lst[8] and lst[8] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif lst[0] == lst[4] == lst[8] and lst[8] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif lst[2] == lst[4] == lst[6] and lst[6] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif lst[3] == lst[4] == lst[5] and lst[4] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif lst[2] == lst[5] == lst[8] and lst[5] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif lst[1] == lst[4] == lst[7] and lst[4] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif lst[6] == lst[7] == lst[8] and lst[6] in ["❌", "⭕️"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ты победил!",
                reply_markup=markup,
            )
            return MAINMENU
        elif context.user_data["h"] == 9:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="Ничья!", reply_markup=markup
            )
            return MAINMENU
    # игра продолжается
    keyboard = [
        [
            InlineKeyboardButton(lst[0], callback_data="0"),
            InlineKeyboardButton(lst[1], callback_data="1"),
            InlineKeyboardButton(lst[2], callback_data="2"),
        ],
        [
            InlineKeyboardButton(lst[3], callback_data="3"),
            InlineKeyboardButton(lst[4], callback_data="4"),
            InlineKeyboardButton(lst[5], callback_data="5"),
        ],
        [
            InlineKeyboardButton(lst[6], callback_data="6"),
            InlineKeyboardButton(lst[7], callback_data="7"),
            InlineKeyboardButton(lst[8], callback_data="8"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Ход крестиков.",
        reply_markup=markup,
    )
    if context.user_data["h"] % 2 != 0:
        await query.edit_message_text(
            text="Ход ноликов.",
            reply_markup=markup,
        )
