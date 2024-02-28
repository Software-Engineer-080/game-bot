import sqlite3
import datetime
from telebot import TeleBot, types
from yookassa import Configuration

bot = TeleBot('')

yootoken = ''

Configuration.account_id = ''
Configuration.secret_key = ''

conn = sqlite3.connect('game.sqlite', check_same_thread=False)


class User:
    def __init__(self, name, user_id, money=40, status='Новичок', wins=0):
        self.name = name
        self.id = user_id
        self.money = money
        self.status = status
        self.wins = wins

    def update_money(self):
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET money = ?, status = ?, wins = ? WHERE user_id = ?",
                       (self.money, self.status, self.wins, self.id))
        conn.commit()
        cursor.close()

    def update_wins(self):
        self.wins += 1
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET money = ?, status = ?, wins = ? WHERE user_id = ?",
                       (self.money, self.status, self.wins, self.id))
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
        return f'----🌚 Информация 🌝----\n\n' \
               f'┏ 🎖️Статус: {self.status}\n\n' \
               f'┣ 🔑ID: {self.id}\n\n' \
               f'┣ 💁Имя: {self.name}\n\n' \
               f'┣ 🏆Победы: {self.wins}\n\n' \
               f'┗ 💳Монеты: {self.money}💰'


# Функция создания пользователя и добавления его в БД

def get_or_create_user(user_id, name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        user = User(existing_user[2], existing_user[1], existing_user[3], existing_user[4], existing_user[5])
    else:
        cursor.execute('INSERT INTO users (user_id, name, money, status, wins) VALUES (?, ?, ?, ?, ?)',
                       (user_id, name, 40, 'Новичок', 0))
        conn.commit()
        user = User(name, user_id, 40, 'Новичок', 0)
    cursor.close()
    return user


# Функция обновления статуса пользователя

def update_status(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT wins FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result is not None:
        wins = result[0]
        cursor.close()

        if wins < 100:
            new_status = 'Новичок'
        elif 100 <= wins < 2000:
            new_status = 'Геймер'
        elif 2000 <= wins < 5000:
            new_status = 'Мастер'
        elif 5000 <= wins < 10000:
            new_status = 'Ветеран'
        elif 10000 <= wins < 100000:
            new_status = 'Завоеватель'
        else:
            new_status = 'БОГ'

        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = ? WHERE user_id = ?", (new_status, user_id))
        conn.commit()
        cursor.close()
    else:
        print("Пользователь с таким user_id не найден.")


# Функция проверки баланса пользователей перед играми

def check_money(call, user, amount):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=(f'Вы не можете сыграть!\n\n'
                                f'Ваш баланс монет: {user.money}💰\n\n'
                                f'Для игры нужно {amount}💰\n\n'
                                f'Купите 💰 в профиле!'),
                          reply_markup=inline_buttons(["В меню ↘️"]))


# Функция создания клавиатуры кнопок под текстом

def inline_buttons(buttons_lst, buttons_per_row=2):
    markup = types.InlineKeyboardMarkup()
    for i in range(0, len(buttons_lst), buttons_per_row):
        button_row = []
        for j in range(buttons_per_row):
            if i + j < len(buttons_lst):
                button_row.append(
                    types.InlineKeyboardButton(text=buttons_lst[i + j], callback_data=buttons_lst[i + j]))
        markup.row(*button_row)
    return markup


# Функция по выводу меню пользователя / админа

def account(message, user):
    if (user.id == 6700989923) or (user.id == 517899909):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_1 = types.InlineKeyboardButton(text='ADMIN', callback_data='ADMIN')
        btn_2 = types.InlineKeyboardButton(text='Купить 💰', callback_data='Купить 💰',
                                           url='https://yookassa.ru/my/i/ZdzHrtzVqUxt/l')
        btn_3 = types.InlineKeyboardButton(text='Передать 💶', callback_data='Передать 💶')
        btn_4 = types.InlineKeyboardButton(text='В меню ↘️', callback_data='В меню ↘️')
        markup.add(btn_1, btn_2, btn_3, btn_4)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_1 = types.InlineKeyboardButton(text='Купить 💰', callback_data='Купить 💰',
                                           url='https://yookassa.ru/my/i/ZdzHrtzVqUxt/l')
        btn_2 = types.InlineKeyboardButton(text='Продать 💸', callback_data='Продать 💸')
        btn_3 = types.InlineKeyboardButton(text='Передать 💶', callback_data='Передать 💶')
        btn_4 = types.InlineKeyboardButton(text='В меню ↘️', callback_data='В меню ↘️')
        markup.add(btn_1, btn_2, btn_3, btn_4)
    update_status(message.chat.id)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text=user.get_info(), reply_markup=markup)


# Функция админа по просмотру количества пользователей

def users_count(message):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    cursor.close()

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    bot.edit_message_text(
        f"Пользователи: {count}\n\nВремя: {current_time}",
        chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=inline_buttons(['Стат 🌪', "Users", '❌', '☯️', 'Вернуться ☝🏻'])
    )


# Функция админа по просмотру информации о пользователях в БД

def admin_users(call, page=1, items_per_page=3):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users_info = cursor.fetchall()
    cursor.close()
    update_status(call.from_user.id)

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_users = users_info[start_index:end_index]

    all_user = ''
    for user_info in current_page_users:
        a_id, user_id, name, money, status, wins = user_info
        user_info_text = (f"┏🆔: {user_id}\n"
                          f"┣🃏: {name}\n"
                          f'┣⚛️: {status}\n'
                          f'┣🎖️: {wins}\n'
                          f"┗💰: {money}\n\n")
        all_user += user_info_text

    if call.message:
        markup = types.InlineKeyboardMarkup()
        total_pages = (len(users_info) + items_per_page - 1) // items_per_page

        if page > 1:
            btn_1 = types.InlineKeyboardButton(text='⬅️', callback_data=f'prev_{page}')
        else:
            btn_1 = types.InlineKeyboardButton(text='⬅️', callback_data=f'prev_{total_pages + 1}')

        btn_2 = types.InlineKeyboardButton(text=f'{page}/{total_pages}', callback_data=' ')

        if page < total_pages:
            btn_3 = types.InlineKeyboardButton(text='➡️', callback_data=f'next_{page}')
        else:
            btn_3 = types.InlineKeyboardButton(text='➡️', callback_data=f'next_0')

        markup.row(btn_1, btn_2, btn_3)
        btn_4 = types.InlineKeyboardButton(text='К админке ⚖️', callback_data='К админке ⚖️')
        markup.row(btn_4)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=all_user,
                              reply_markup=markup)

    else:
        bot.send_message(call.message.chat.id, "Сообщение для редактирования не найдено")


# Функция админа по передаче монет

def transfer_now(message):
    sent_message = bot.send_message(message.chat.id, "Введите: 'ID-сумма'")
    bot.register_next_step_handler(sent_message, transfer_next)


def transfer_next(message):
    try:
        user_id, amount = map(int, message.text.split('-'))
        receiver = get_or_create_user(user_id, "Unknown")
        receiver.add_money(amount)
        if (user_id == 6700989923) or (user_id == 517899909):
            bot.send_message(message.chat.id, f"Вы закинули себе {amount}💰")
        else:
            bot.send_message(user_id, f"Админ пополнил ваш счет на {amount}💰")
            bot.send_message(message.chat.id, f"Вы передали {amount}💰\nпользователю {user_id}\n\n"
                                              f"Нажмите заново /start", )
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат сообщения. Попробуйте снова")


# Функции отправки сообщения конкретному пользователю от админа

def send_user(message):
    sent_message = bot.send_message(message.chat.id, "Введите: 'ID - текст'")
    bot.register_next_step_handler(sent_message, go_user)


def go_user(message):
    try:
        user_id, text = message.text.split(' - ')
        bot.send_message(user_id, f'Вам сообщение от 👨‍💻:\n\n'
                                  f'{text}')
        bot.send_message(message.chat.id, f'Сообщение отправлено пользователю с ID-{user_id}')
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат сообщения. Попробуйте снова")


# Функции отправки сообщения всем пользователям в БД (Рассылка)

def all_send(message):
    sent_message = bot.send_message(message.chat.id, "Введи текст рассылки и не забудь {}:")
    bot.register_next_step_handler(sent_message, all_go)


def all_go(message):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users_info = cursor.fetchall()
    cursor.close()
    update_status(message.from_user.id)
    text = message.text
    try:
        for user_info in users_info:
            if user_info[1] != message.from_user.id:
                bot.send_message(user_info[1], text.format(user_info[2]))
        bot.send_message(message.chat.id, "Рассылка отправлена всем пользователям бота!")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат сообщения!\n\n"
                                          "Рассылка не ушла! Попробуй еще!")


# Функции пользователей по передаче монет друг другу

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
