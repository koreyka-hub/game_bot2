from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def make_keyboard_ttt(board: list):
    keyboard = [
        [
            InlineKeyboardButton(board[0], callback_data="0"),
            InlineKeyboardButton(board[1], callback_data="1"),
            InlineKeyboardButton(board[2], callback_data="2"),
        ],
        [
            InlineKeyboardButton(board[3], callback_data="3"),
            InlineKeyboardButton(board[4], callback_data="4"),
            InlineKeyboardButton(board[5], callback_data="5"),
        ],
        [
            InlineKeyboardButton(board[6], callback_data="6"),
            InlineKeyboardButton(board[7], callback_data="7"),
            InlineKeyboardButton(board[8], callback_data="8"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    return markup