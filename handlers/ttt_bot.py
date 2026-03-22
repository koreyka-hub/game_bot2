from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.states import MAINMENU, TICTACTOE_BOT
from openai import AsyncOpenAI

from db.games_crud import add_games, get_games


async def tictactoe_bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    games = await get_games(update.effective_user.id)
    print(games['id'], games['user_tg_id'])
    if not games:
        await add_games(update.effective_user.id, update.effective_user.id)

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
    query = update.callback_query
    await query.answer()

    i = context.user_data['i']
    nomer_knopki = int(query.data)
    lst = context.user_data["lst"]
    if lst[nomer_knopki] == '⬜':
        lst[nomer_knopki] = i
        context.user_data['h'] += 1
    
    # игра продолжается
    keyboard = [
        [
            InlineKeyboardButton(lst[0], callback_data="pep"),
            InlineKeyboardButton(lst[1], callback_data="shnele"),
            InlineKeyboardButton(lst[2], callback_data="watafa"),
        ],
        [
            InlineKeyboardButton(lst[3], callback_data="fafa"),
            InlineKeyboardButton(lst[4], callback_data="fa"),
            InlineKeyboardButton(lst[5], callback_data="famen"),
        ],
        [
            InlineKeyboardButton(lst[6], callback_data="fawomen"),
            InlineKeyboardButton(lst[7], callback_data="famail"),
            InlineKeyboardButton(lst[8], callback_data="fahon"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="GPT думает...",
        reply_markup=markup,
    )
    # тут пошла история с gpt

    client = AsyncOpenAI()
    response = await client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": 'ты бот,играющий в крестики нолики.Играй с игроком по правилам игры,ты играешь за нолики. Игрок кидает тебе текущее положение на доске в виде строки из 9 символов, каждые 3 символа это строка поля. Если есть свободные клетки,то в ответе укажи только одно ЧИСЛО от 0 до 8 - это клетка куда нужно походить. ',
            },
            {
                "role": "user",
                "content": "".join(context.user_data["lst"]),
            }
        ],
    )
    response_text = response.output_text
    
    lst[int(response_text)] = '⭕️'
    context.user_data['h'] += 1

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
        text="Твой ход.",
        reply_markup=markup,
    )
    
    keyboard = [
            [InlineKeyboardButton("играть заново", callback_data="bot_tictactoe")],
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
    elif context.user_data["h"] == 8:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ничья!", reply_markup=markup
        )
        return MAINMENU
