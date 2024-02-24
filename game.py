from telebot import TeleBot, types
import sqlite3
import alive
import logging
import datetime
from time import sleep
from games_1 import casino, casino_fire
from games_2 import stone_game, stone, scissors, paper
from games_3 import tails, verify
from game_dice import dice, dice_min, dice_three, dice_max
import game_21
from yookassa import Configuration, Payment

bot = TeleBot('6739834598:AAGfsRZZyrn2-ki5BgOdYeZWm5OUfh6UJxw')

yootoken = '390540012:LIVE:46917'

Configuration.account_id = '337976'
Configuration.secret_key = 'test_nLq_kHuSF_E9J-_c-2-vxtvqXsSDVgGXB0Kcg6UwnkE'

conn = sqlite3.connect('game.sqlite', check_same_thread=False)


class User:
    def __init__(self, name, user_id, money=35, status='Новичок', wins=0):
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
        return f'🌚Информация🌝\n\n' \
               f'Статус: {self.status}\n\n'\
               f'Победы: {self.wins}\n\n'\
               f'Имя: {self.name}\n\n' \
               f'ID: {self.id}\n\n' \
               f'Монеты: {self.money}💰'


def admin_users(call):
    if call.from_user.id == 517899909:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users_info = cursor.fetchall()
        cursor.close()
        update_status(call.from_user.id)
        all_user = ''
        for user_info in users_info:
            a_id, user_id, name, money, status, wins = user_info
            user_info_text = (f"🆔: {user_id}\n"
                              f"🃏: {name}\n"
                              f'⚛️: {status}\n'
                              f'🎖️: {wins}\n'
                              f"💰: {money}\n\n")
            all_user += user_info_text

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        all_user += f"Время: {current_time}"

        if call.message:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=all_user,
                                  reply_markup=inline_buttons(['Стат 🌪', "Users", 'STOP ❌', 'Вернуться ☝🏻']))

        else:
            bot.send_message(call.message.chat.id, "Сообщение для редактирования не найдено")


def get_or_create_user(user_id, name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        user = User(existing_user[2], existing_user[1], existing_user[3], existing_user[4], existing_user[5])
    else:
        cursor.execute('INSERT INTO users (user_id, name, money, status, wins) VALUES (?, ?, ?, ?, ?)',
                       (user_id, name, 35, 'Новичок', 0))
        conn.commit()
        user = User(name, user_id, 35, 'Новичок', 0)
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
        reply_markup=inline_buttons(['Стат 🌪', "Users", 'STOP ❌', 'Вернуться ☝🏻'])
    )


def transfer_now(message):
    sent_message = bot.send_message(message.chat.id, "Введите: 'ID-сумма'")
    bot.register_next_step_handler(sent_message, transfer_next)


def transfer_next(message):
    try:
        user_id, amount = map(int, message.text.split('-'))
        receiver = get_or_create_user(user_id, "Unknown")
        receiver.add_money(amount)
        if user_id != 517899909:
            bot.send_message(user_id, f"Админ пополнил ваш счет на {amount}💰")
            bot.send_message(message.chat.id, f"Вы передали {amount} монет пользователю с ID {user_id}\n\n"
                                              f"Нажмите заново /start", )
        else:
            bot.send_message(message.chat.id, f"Вы пополнили свой счет на {amount}💰")
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
            new_status = 'Сталкер'
        elif 2000 <= wins < 5000:
            new_status = 'Ветеран'
        elif 5000 <= wins < 10000:
            new_status = 'Мастер'
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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", [user_id])
    exists = cursor.fetchone()
    if not exists:
        cursor.execute('INSERT INTO users (user_id, name, money, status, wins) VALUES (?, ?, ?, ?, ?)',
                       (user_id, message.from_user.first_name, 35, 'Новичок', 0))
        conn.commit()
        bot.send_message(517899909, f'⚡️Пользователь {message.from_user.first_name} воспользовался ботом⚡️')
        bot.send_message(message.chat.id,
                         f'Приветствую, {message.from_user.first_name} 👋🏻\n\n'
                         f'Я твой бот для развлечений!\n\n'
                         f'И готов помочь тебе повеселиться 🎮!\n\n'
                         f'Выбери желаемую кнопку меню 👇🏻',
                         reply_markup=inline_buttons(
                             ["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", 'Кости 🎲', '21🃏', "Казино 🎰"]))
    else:
        bot.send_message(message.chat.id, f'Рад, что Вы вернулись, {message.from_user.first_name}!',
                         reply_markup=inline_buttons(
                             ["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", 'Кости 🎲', '21🃏', "Казино 🎰"]))
    cursor.close()


def account(message, user):
    if user.id == 517899909:
        user_menu = inline_buttons(['ADMIN', "Пополнить счёт", 'Передать 💰', 'В меню ↘️'], buttons_per_row=2)
    else:
        user_menu = inline_buttons(["Пополнить счёт", 'Продать 💸', 'Передать 💰', 'В меню ↘️'],
                                   buttons_per_row=2)
    update_status(message.chat.id)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text=user.get_info(), reply_markup=user_menu)


def pay(message):
    bot.send_invoice(message.chat.id,
                     title="Покупка токенов",
                     description='100 рублей --> 50 токенов',
                     invoice_payload="Payment: Zozulya Yaroslav",
                     currency="RUB",
                     max_tip_amount=10000,
                     suggested_tip_amounts=[20 * 10, 30 * 10, 40 * 10],
                     provider_token=yootoken,
                     photo_url='https://i.ibb.co/t3L4fYL/tokens.png',
                     photo_width=150,
                     photo_height=150,
                     photo_size=78,
                     need_name=True,
                     is_flexible=False,
                     prices=[types.LabeledPrice(label="50 💰", amount=100 * 100)],
                     start_parameter="payment")


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    bot.answer_shipping_query(shipping_query.id, ok=True)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Error")


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    user_id = message.from_user.id
    amount = 50
    payment = Payment.create({
        "amount": {
            "value": str(amount * 2),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/All_Funny_Games_bot"
        },
        'capture': True,
        "description": "Покупка токенов для бота"
    })
    user = get_or_create_user(user_id, message.from_user.first_name)
    if payment.status == 'succeeded':
        user.add_money(amount)
        bot.send_message(message.from_user.id, f'Вы успешно приобрели {amount} токенов\n'
                                               f'Нажмите заново /start')


game_instance = game_21.BlackjackGame()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global game_instance
    logging.debug(f"Received callback query: {call.data}")

    user_id = call.from_user.id
    user = get_or_create_user(user_id, call.from_user.first_name)

    if call.data == "Профиль":
        account(call.message, user)
    elif call.data == "Орёл / Решка":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=tails(), reply_markup=inline_buttons(["Орёл 🦅", "Решка 🪙", "В меню ↘️"]))
    elif call.data == "✊🏻/✌🏻/✋🏻":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=stone_game(), reply_markup=inline_buttons(["✊🏻", "✌🏻", "✋🏻", "В меню ↘️"]))
    elif call.data == "Казино 🎰":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=casino(), reply_markup=inline_buttons(["Запуск 🔥", "В меню ↘️"]))
    elif call.data == 'Кости 🎲':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=dice(), reply_markup=inline_buttons(["🎲 < 3", "🎲 = 3", "🎲 > 3", "В меню ↘️"]))
    elif (call.data == '21🃏') or (call.data == 'К игре ⬆️'):
        game_instance = game_21.BlackjackGame()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=game_instance.start_card(),
                              reply_markup=inline_buttons(["Играть ⏯️", "Правила 📝", "В меню ↘️"]))
    elif call.data == "Пополнить счёт":
        pay(call.message)
    elif call.data == "Передать 💰":
        if user_id == 517899909:
            transfer_now(call.message)
        else:
            transfer_money_now(call.message)
    elif call.data == "ADMIN":
        if user_id == 517899909:
            bot.edit_message_text("Меню ADMIN",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=inline_buttons(['Стат 🌪', "Users", 'STOP ❌', 'Вернуться ☝🏻']))

    elif call.data == "Стат 🌪":
        users_count(call.message)
    elif call.data == "Users":
        admin_users(call)
    elif call.data == 'STOP ❌':
        bot.stop_bot()
    elif call.data == 'Орёл 🦅':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=verify(call, user), reply_markup=inline_buttons(["Орёл 🦅", "Решка 🪙", "В меню ↘️"]))
    elif call.data == 'Решка 🪙':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=verify(call, user), reply_markup=inline_buttons(["Орёл 🦅", "Решка 🪙", "В меню ↘️"]))
    elif call.data == 'Запуск 🔥':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=casino_fire(user), reply_markup=inline_buttons(["Запуск 🔥", "В меню ↘️"]))
    elif call.data == '✊🏻':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=stone(user), reply_markup=inline_buttons(["✊🏻", "✌🏻", "✋🏻", "В меню ↘️"]))
    elif call.data == '✌🏻':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=scissors(user), reply_markup=inline_buttons(["✊🏻", "✌🏻", "✋🏻", "В меню ↘️"]))
    elif call.data == '✋🏻':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=paper(user), reply_markup=inline_buttons(["✊🏻", "✌🏻", "✋🏻", "В меню ↘️"]))
    elif call.data == '🎲 < 3':
        dice_1 = bot.send_dice(call.message.chat.id)
        sleep(3)
        bot.send_message(chat_id=call.message.chat.id,
                         text=dice_min(dice_1, user),
                         reply_markup=inline_buttons(["🎲 < 3", "🎲 = 3", "🎲 > 3", "В меню ↘️"]))
    elif call.data == '🎲 = 3':
        dice_2 = bot.send_dice(call.message.chat.id)
        sleep(3)
        bot.send_message(chat_id=call.message.chat.id,
                         text=dice_three(dice_2, user),
                         reply_markup=inline_buttons(["🎲 < 3", "🎲 = 3", "🎲 > 3", "В меню ↘️"]))
    elif call.data == '🎲 > 3':
        dice_3 = bot.send_dice(call.message.chat.id)
        sleep(3)
        bot.send_message(chat_id=call.message.chat.id,
                         text=dice_max(dice_3, user),
                         reply_markup=inline_buttons(["🎲 < 3", "🎲 = 3", "🎲 > 3", "В меню ↘️"]))
    elif call.data == 'Правила 📝':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=game_instance.rules(), reply_markup=inline_buttons(["К игре ⬆️"]))
    elif call.data == 'Играть ⏯️' or (call.data == 'Сыграть ещё'):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=game_instance.start(),
                              reply_markup=inline_buttons(["5💰", "10💰", "15💰", "20💰", "К игре ⬆️"]))

    elif call.data in ['5💰', '10💰', '15💰', '20💰']:
        amount = int(call.data.replace('💰', ''))
        game_text = game_instance.game(user=user, amount=amount)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=game_text, reply_markup=inline_buttons(["Ещё", "Стоп"]))

    elif call.data == 'Ещё':
        add_card_text = game_instance.add_card()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=add_card_text, reply_markup=inline_buttons(["Ещё", "Стоп"]))
    elif call.data == 'Стоп':
        stop_text = game_instance.stop_card(user)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=stop_text, reply_markup=inline_buttons(['Сыграть ещё', "В меню ↘️"]))
    elif call.data == 'В меню ↘️':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text='Вы в главном меню!',
                              reply_markup=inline_buttons(
                                  ["Профиль", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", 'Кости 🎲', '21🃏', "Казино 🎰"]))
    elif call.data == 'Вернуться ☝🏻':
        account(call.message, user)
    else:
        bot.answer_callback_query(call.id, text='Команда в разработке!')


alive.keep_alive()
bot.polling(none_stop=True, interval=0)
