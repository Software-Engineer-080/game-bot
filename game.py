from telebot import TeleBot, types
import sqlite3
import alive
from games_1 import casino, casino_fire
from games_2 import stone_game, stone, scissors, paper
from games_3 import tails, verify

bot = TeleBot('6739834598:AAGfsRZZyrn2-ki5BgOdYeZWm5OUfh6UJxw')

conn = sqlite3.connect('game.sqlite', check_same_thread=False)
cursor = conn.cursor()


class User:
    def __init__(self, name, user_id, money=35):
        self.name = name
        self.id = user_id
        self.money = money

    def update_money(self):
        cursor.execute("UPDATE users SET money = ? WHERE user_id = ?", (self.money, self.id))
        conn.commit()

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


def admin_users(message):
    if message.from_user.id == 517899909:
        cursor.execute("SELECT * FROM users")
        users_info = cursor.fetchall()
        all_user = ''
        for user_info in users_info:
            a_id, user_id, name, money = user_info
            user_info_text = (f"🆔: {user_id}\n"
                              f"🃏: {name}\n"
                              f"💰: {money}\n\n")
            all_user += user_info_text
        bot.send_message(message.chat.id, f'{all_user}')
    else:
        bot.send_message(message.chat.id, "У вас нет прав доступа к этой команде.")


def get_or_create_user(user_id, name):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        user = User(existing_user[2], existing_user[1], existing_user[3])
    else:
        cursor.execute('INSERT INTO users (user_id, name, money) VALUES (?, ?, ?)', (user_id, name, 35))
        conn.commit()
        user = User(name, user_id, 35)
    return user


def users_count(message):
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    bot.send_message(message.chat.id, f"Пользователи: {count}")


def transfer_now(message):
    bot.send_message(message.chat.id, "Введите: 'ID-сумма'")
    bot.register_next_step_handler(message, transfer_next)


def transfer_next(message):
    try:
        user_id, amount = map(int, message.text.split('-'))
        receiver = get_or_create_user(user_id, "Unknown")
        receiver.add_money(amount)
        bot.send_message(message.chat.id, f"Вы передали {amount} монет пользователю с ID {user_id}")
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

        if sender.money >= amount:
            sender.deduct_money(amount)
            receiver.add_money(amount)
            bot.send_message(message.chat.id, f"Вы передали {amount} монет пользователю с ID {user_id}")
        else:
            bot.send_message(message.chat.id, "Недостаточно монет для передачи")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат сообщения. Попробуйте снова")


def buttons(buttons_lst):
    lst = []
    for button in buttons_lst:
        lst.append(types.KeyboardButton(text=button))

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*lst)
    return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
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
                         reply_markup=buttons(["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", "Казино 🎰"]))
    else:
        bot.send_message(message.chat.id, f'Рад, что Вы вернулись, {message.from_user.first_name}!',
                         reply_markup=buttons(["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", "Казино 🎰"]))


def account(message, user):
    if message.from_user.id == 517899909:
        user_menu = buttons(['ADMIN', "Пополнить счёт", 'Передать 💰', 'В главное меню!'])

    else:
        user_menu = buttons(["Пополнить счёт", 'Передать 💰', 'В главное меню!'])
    bot.send_message(message.chat.id, user.get_info(), reply_markup=user_menu)


@bot.message_handler(content_types=['text'])
def send_text(message):
    user = get_or_create_user(message.from_user.id, message.from_user.first_name)
    if message.text == 'Профиль':
        account(message, user)
    elif message.text == 'Орёл / Решка':
        bot.send_message(message.chat.id, tails(), reply_markup=buttons(["Орёл 🦅", "Решка 🪙", "В главное меню!"]))
    elif message.text == '✊🏻/✌🏻/✋🏻':
        bot.send_message(message.chat.id, stone_game(), reply_markup=buttons(["✊🏻", "✌🏻", "✋🏻", "В главное меню!"]))
    elif message.text == 'Казино 🎰':
        bot.send_message(message.chat.id, casino(), reply_markup=buttons(["Запуск 🔥", "В главное меню!"]))
    elif message.text == 'Пополнить счёт':
        if message.from_user.id == 517899909:
            transfer_now(message)
        else:
            pass
    elif message.text == 'Передать 💰':
        transfer_money_now(message)
    elif message.text == 'ADMIN':
        if message.from_user.id == 517899909:
            bot.send_message(message.chat.id, '🔮🔮🔮', reply_markup=buttons(['Стат 🌪', "Users", 'Вернуться ☝🏻']))
    elif message.text == 'Стат 🌪':
        users_count(message)
    elif message.text == "Users":
        admin_users(message)
    elif message.text == 'Орёл 🦅':
        bot.send_message(message.chat.id, verify(message, user))
    elif message.text == 'Решка 🪙':
        bot.send_message(message.chat.id, verify(message, user))
    elif message.text == 'Запуск 🔥':
        bot.send_message(message.chat.id, casino_fire(user))
    elif message.text == '✊🏻':
        bot.send_message(message.chat.id, stone(user))
    elif message.text == '✌🏻':
        bot.send_message(message.chat.id, scissors(user))
    elif message.text == '✋🏻':
        bot.send_message(message.chat.id, paper(user))
    elif message.text == 'В главное меню!':
        bot.send_message(message.chat.id, 'Вы в главном меню!',
                         reply_markup=buttons(["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", "Казино 🎰"]))
    elif message.text == 'Вернуться ☝🏻':
        account(message, user)
    else:
        bot.send_message(message.chat.id, 'На такую команду я не запрограммирован!')


alive.keep_alive()
bot.polling(none_stop=True, interval=0)
