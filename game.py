from telebot import TeleBot, types
import sqlite3
import alive
import logging
import datetime
from games_1 import casino, casino_fire
from games_2 import stone_game, stone, scissors, paper
from games_3 import tails, verify

bot = TeleBot('6739834598:AAGfsRZZyrn2-ki5BgOdYeZWm5OUfh6UJxw')

conn = sqlite3.connect('game.sqlite', check_same_thread=False)


class User:
    def __init__(self, name, user_id, money=35):
        self.name = name
        self.id = user_id
        self.money = money

    def update_money(self):
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET money = ? WHERE user_id = ?", (self.money, self.id))
        conn.commit()
        cursor.close()

    def add_money(self, amount):
        self.money += amount
        self.update_money()

    def deduct_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            self.update_money()

    def get_info(self):
        return f'🌚Информация🌝\n\n' \
               f'Имя: {self.name}\n' \
               f'ID: {self.id}\n' \
               f'Монеты: {self.money}💰'


def admin_users(call):
    if call.from_user.id == 517899909:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users_info = cursor.fetchall()
        cursor.close()

        all_user = ''
        for user_info in users_info:
            a_id, user_id, name, money = user_info
            user_info_text = (f"🆔: {user_id}\n"
                              f"🃏: {name}\n"
                              f"💰: {money}\n\n")
            all_user += user_info_text

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        all_user += f"Время: {current_time}"

        if call.message:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=all_user,
                                  reply_markup=inline_buttons(['Стат 🌪', "Users", 'Вернуться ☝🏻']))

        else:
            bot.send_message(call.message.chat.id, "Сообщение для редактирования не найдено")


def get_or_create_user(user_id, name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        user = User(existing_user[2], existing_user[1], existing_user[3])
    else:
        cursor.execute('INSERT INTO users (user_id, name, money) VALUES (?, ?, ?)',
                       (user_id, name, 35))
        conn.commit()
        user = User(name, user_id, 35)
    cursor.close()
    return user


def users_count(message):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    cursor.close()

    bot.edit_message_text(
        f"Пользователи: {count}",
        chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=inline_buttons(['Стат 🌪', "Users", 'Вернуться ☝🏻'])
    )


def transfer_now(message):
    sent_message = bot.send_message(message.chat.id, "Введите: 'ID-сумма'")
    bot.register_next_step_handler(sent_message, transfer_next)


def transfer_next(message):
    try:
        user_id, amount = map(int, message.text.split('-'))
        receiver = get_or_create_user(user_id, "Unknown")
        receiver.add_money(amount)
        bot.send_message(user_id, f"Админ пополнил вас счет на {amount}💰")
        bot.send_message(message.chat.id, f"Вы передали {amount} монет пользователю с ID {user_id}\n\n"
                                          f"Нажмите заново /start", )
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат сообщения. Попробуйте снова")


def transfer_money_now(message):
    bot.send_message(message.chat.id, "Введите: 'ID-сумма'")
    bot.register_next_step_handler(message, transfer_money_next)


def transfer_money_next(message):
    try:
        user_id, amount = map(int, message.text.split('-'))
        sender_id = message.from_user.id
        sender = get_or_create_user(sender_id, "Unknown")
        receiver = get_or_create_user(user_id, "Unknown")
        if sender_id != user_id:
            if sender.money >= amount:
                sender.deduct_money(amount)
                receiver.add_money(amount)
                bot.send_message(message.chat.id, f"Вы передали {amount} монет пользователю с ID {user_id}\n\n"
                                                  f"Нажмите заново /start", )
            else:
                bot.send_message(message.chat.id, "Недостаточно монет для передачи")
        else:
            bot.send_message(message.chat.id, "Вы не можете передать себе 💰!\n\nПопробуйте еще раз!'")
            transfer_money_now(message)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат сообщения. Попробуйте снова")


def inline_buttons(buttons_lst, buttons_per_row=2):
    markup = types.InlineKeyboardMarkup()
    for i in range(0, len(buttons_lst), buttons_per_row):
        button_row = []
        for j in range(buttons_per_row):
            if i + j < len(buttons_lst):
                button_row.append(types.InlineKeyboardButton(text=buttons_lst[i + j], callback_data=buttons_lst[i + j]))
        markup.row(*button_row)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", [user_id])
    exists = cursor.fetchone()
    if not exists:
        cursor.execute('INSERT INTO users (user_id, name, money) VALUES (?, ?, ?)',
                       (message.from_user.id, message.from_user.first_name, 35))
        conn.commit()
        bot.send_message(517899909, f'⚡️Пользователь {message.from_user.first_name} воспользовался ботом⚡️')
        bot.send_message(message.chat.id,
                         f'Приветствую, {message.from_user.first_name} 👋🏻\n\n'
                         f'Я твой бот для развлечений!\n\n'
                         f'И готов помочь тебе повеселиться 🎮!\n\n'
                         f'Выбери желаемую кнопку меню 👇🏻',
                         reply_markup=inline_buttons(["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", "Казино 🎰"]))
    else:
        bot.send_message(message.chat.id, f'Рад, что Вы вернулись, {message.from_user.first_name}!',
                         reply_markup=inline_buttons(["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", "Казино 🎰"]))
    cursor.close()


def account(message, user):
    if user.id == 517899909:
        user_menu = inline_buttons(['ADMIN', "Пополнить счёт", 'Передать 💰', 'В меню!'], buttons_per_row=2)
    else:
        user_menu = inline_buttons(["Пополнить счёт", 'Продать 💸', 'Передать 💰', 'В меню!'],
                                   buttons_per_row=2)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text=user.get_info(), reply_markup=user_menu)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    logging.debug(f"Received callback query: {call.data}")

    user_id = call.from_user.id
    user = get_or_create_user(user_id, call.from_user.first_name)

    if call.data == "Профиль":
        account(call.message, user)
    elif call.data == "Орёл / Решка":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=tails(), reply_markup=inline_buttons(["Орёл 🦅", "Решка 🪙", "В меню!"]))
    elif call.data == "✊🏻/✌🏻/✋🏻":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=stone_game(), reply_markup=inline_buttons(["✊🏻", "✌🏻", "✋🏻", "В меню!"]))
    elif call.data == "Казино 🎰":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=casino(), reply_markup=inline_buttons(["Запуск 🔥", "В меню!"]))
    elif call.data == "Пополнить счёт":
        if user_id == 517899909:
            transfer_now(call.message)
        else:
            pass
    elif call.data == "Передать 💰":
        transfer_money_now(call.message)
    elif call.data == "ADMIN":
        if user_id == 517899909:
            bot.edit_message_text("Меню ADMIN",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=inline_buttons(['Стат 🌪', "Users", 'Вернуться ☝🏻']))

    elif call.data == "Стат 🌪":
        users_count(call.message)
    elif call.data == "Users":
        admin_users(call)
    elif call.data == 'Орёл 🦅':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=verify(call, user), reply_markup=inline_buttons(["Орёл 🦅", "Решка 🪙", "В меню!"]))
    elif call.data == 'Решка 🪙':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=verify(call, user), reply_markup=inline_buttons(["Орёл 🦅", "Решка 🪙", "В меню!"]))
    elif call.data == 'Запуск 🔥':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=casino_fire(user), reply_markup=inline_buttons(["Запуск 🔥", "В меню!"]))
    elif call.data == '✊🏻':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=stone(user), reply_markup=inline_buttons(["✊🏻", "✌🏻", "✋🏻", "В меню!"]))
    elif call.data == '✌🏻':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=scissors(user), reply_markup=inline_buttons(["✊🏻", "✌🏻", "✋🏻", "В меню!"]))
    elif call.data == '✋🏻':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=paper(user), reply_markup=inline_buttons(["✊🏻", "✌🏻", "✋🏻", "В меню!"]))
    elif call.data == 'В меню!':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text='Вы в главном меню!',
                              reply_markup=inline_buttons(["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", "Казино 🎰"]))
    elif call.data == 'Вернуться ☝🏻':
        account(call.message, user)
    else:
        bot.answer_callback_query(call.id, text='Команда в разработке!')


alive.keep_alive()
bot.polling(none_stop=True, interval=0)
