from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config.states import TICTACTOE_ONLINE

async def tictactoe_online_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    
    query = update.callback_query
    await query.answer()

    queue = context.bot_data["queue"]
    if len(queue) == 0:
        queue.append(update.effective_user.id)
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Ты добавлен в очередь. Жди пока кто-то зайдет в игру.",
        )
    elif len(queue) >= 1:
        first_user = queue.pop()
        second_user = update.effective_user.id
        game_id = context.bot_data["last_game_id"] + 1
        context.bot_data["games"][game_id] = {
            "krestik": first_user,
            "nolik": second_user,
            "board": [
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
            ],
            "hod": 1,
        }
        await context.bot.send_message(
            chat_id=first_user,
            text="Мы нашли тебе игрока.Ты играешь за крестики",
        )
        await context.bot.send_message(
            chat_id=second_user,
            text="Мы нашли тебе игрока.Ты играешь за нолики",
        )

        return TICTACTOE_ONLINE