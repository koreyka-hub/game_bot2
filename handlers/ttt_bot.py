from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.states import TICTACTOE_BOT
from openai import OpenAI
client = OpenAI()


async def tictactoe_bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query  # Полная информация о нажатой кнопке
    await query.answer()  # отвечаем на запрос
    context.user_data['i'] = '❌'
    context.user_data['h'] = 0
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
    return TICTACTOE_BOT


async def tictactoe_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    query = update.callback_query
    await query.answer()
    i = context.user_data['i']
    nomer_knopki = int(query.data)
    lst = context.user_data["lst"]
    if lst[nomer_knopki] == '⬜':
        lst[nomer_knopki] = i
        if i == '❌':
            context.user_data['i'] = '⭕️'
        else:
            context.user_data['i'] = '❌'
        context.user_data['h'] += 1
        # победа
    if len(context.user_data["previous_messages"]) > 6:
        context.user_data["previous_messages"].pop(0)
        context.user_data["previous_messages"].pop(0)
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "medium"},
        input=[
            {
                "role": "developer",
                "content": 'ты бот,играющий в крестики нолики.Играй с игроком по правилам игры и кратко хвали его за каждый ход.Говори только на русском языке',
            },
        ]
        + context.user_data["previous_messages"]
        + [
            {
                "role": "user",
                "content": text,
            }
        ],
    )
    response_text = response.output_text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text,
    )
    context.user_data["previous_messages"].append(
           {"role": "user", "content": text}
    )
    context.user_data["previous_messages"].append(
        {"role": "assistant", "content": response_text}
    )
    
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
    if context.user_data['h'] % 2 != 0:
        await query.edit_message_text(
        text="Ход ноликов.",
        reply_markup=markup,
    )  
    