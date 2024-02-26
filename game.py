import alive
import game_21
import logging
from time import sleep
from work_func import *
from game_money import tails, verify
from game_casino import casino, casino_fire
from game_stone import stone_game, stone, scissors, paper
from game_dice import dice, dice_min, dice_three, dice_max


user_game_instances = {}


# Функция приветствия пользователей при нажатии команды "/start"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", [user_id])
    exists = cursor.fetchone()
    if not exists:
        cursor.execute('INSERT INTO users (user_id, name, money, status, wins) VALUES (?, ?, ?, ?, ?)',
                       (user_id, message.from_user.first_name, 40, 'Новичок', 0))
        conn.commit()
        bot.send_message(6700989923, f'⚡️Пользователь {message.from_user.first_name} воспользовался ботом⚡️')
        bot.send_message(message.chat.id,
                         f'Приветствую, {message.from_user.first_name} 👋🏻\n\n'
                         f'Я твой бот для развлечений!\n\n'
                         f'И готов помочь тебе повеселиться 🎮!\n\n'
                         f'Выбери желаемую кнопку меню 👇🏻',
                         reply_markup=inline_buttons(
                             ["Профиль ℹ️", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", 'Кости 🎲', '21🃏', "Казино 🎰"]))
    else:
        bot.send_message(message.chat.id, f'Рад, что Вы вернулись, {message.from_user.first_name}!',
                         reply_markup=inline_buttons(
                             ["Профиль ℹ️", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", 'Кости 🎲', '21🃏', "Казино 🎰"]))
    cursor.close()


# Функция отправки пользователю информации о боте при нажатии команды "/info"

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id,
                     f'❗️Раздел информации❗️\n\n'
                     f'⚠️Данный бот был создан Российским независимым разработчиком '
                     f'исключительно в развлекательных целях!\n\n'
                     f'⚠️Все решения, принятые Вами в этом боте - '
                     f'Ваш осознанный выбор и администрация бота '
                     f'НЕ НЕСЁТ за него ответственность!\n\n'
                     f'⚠️Нажав одну из кнопок\n"Начать" или "start"\n'
                     f'Вы даёте согласие на обработку персональных данных!\n\n'
                     f'⚠️Все алгоритмы в данном боте построены на РАНДОМЕ, '
                     f'поэтому администрация бота НЕ МОЖЕТ ВЛИЯТЬ на игровой процесс!\n\n'
                     f'⚠️Если Вам понравился данный проект и Вы готовы его поддержать,'
                     f'то смело нажимайте на кнопку внизу\n\n'
                     f'✅Приятной вам игры!',
                     reply_markup=inline_buttons(["💵 Поддержать проект 💵", 'В меню ↘️'], buttons_per_row=1))


# Функция отправки сообщения разработчику по команде "/sup"

@bot.message_handler(commands=['sup'])
def send_dev(message):
    bot.send_message(message.chat.id, "Введите сообщение для разработчика:")
    bot.register_next_step_handler(message, up_dev)


def up_dev(message):
    bot.send_message(6700989923, f'Пользователь {message.from_user.first_name},\n'
                                 f'c ID - {message.chat.id},\n'
                                 f'отправил вам сообщение:\n\n {message.text}')
    bot.send_message(message.chat.id, "Сообщение отправлено разработчику!")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global user_game_instances
    logging.debug(f"Received callback query: {call.data}")

    user_id = call.from_user.id
    user = get_or_create_user(user_id, call.from_user.first_name)

    if user_id not in user_game_instances:
        user_game_instances[user_id] = game_21.BlackjackGame()

    if call.data == "Профиль ℹ️":
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
        if (user_id == 6700989923) or (user_id == 517899909):
            transfer_now(call.message)
        else:
            transfer_money_now(call.message)
    elif (call.data == "ADMIN") or (call.data == 'К админке ⚖️'):
        bot.edit_message_text("Меню ADMIN", call.message.chat.id, call.message.message_id,
                              reply_markup=inline_buttons(
                                  ['Стат 🌪', "Users", 'STOP ❌', 'Сообщение ☯️', 'Вернуться ☝🏻']))

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
                              text=user_game_instances[user_id].rules(), reply_markup=inline_buttons(["К игре ⬆️"]))
    elif call.data == 'Играть ⏯️' or (call.data == 'Сыграть ещё'):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=user_game_instances[user_id].start(),
                              reply_markup=inline_buttons(["6💰", "9💰", "12💰", "15💰", "К игре ⬆️"]))

    elif call.data in ["6💰", "9💰", "12💰", "15💰"]:
        amount = int(call.data.replace('💰', ''))
        game_text = user_game_instances[user_id].game(user=user, amount=amount)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=game_text, reply_markup=inline_buttons(["Ещё", "Хватит"]))

    elif call.data == 'Ещё':
        add_card_text = user_game_instances[user_id].add_card()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=add_card_text, reply_markup=inline_buttons(["Ещё", "Хватит"]))
    elif call.data == 'Хватит':
        stop_text = user_game_instances[user_id].stop_card(user)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=stop_text, reply_markup=inline_buttons(['Сыграть ещё', "В меню ↘️"]))
    elif call.data == 'В меню ↘️':
        update_status(call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text='Вы в главном меню!',
                              reply_markup=inline_buttons(
                                  ["Профиль ℹ️", "Орёл / Решка", "✊🏻/✌🏻/✋🏻", 'Кости 🎲', '21🃏', "Казино 🎰"]))
    elif call.data == 'Вернуться ☝🏻':
        account(call.message, user)
    elif call.data == 'Сообщение ☯️':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='‼️Пользуйся этой кнопкой предельно осторожно, '
                                   'иначе вызовешь недовольство юзеров‼️',
                              reply_markup=inline_buttons(
                                  ['Пользователю ☢️', 'Рассылка 🆘', 'К админке ⚖️'], buttons_per_row=1))
    elif call.data == 'Пользователю ☢️':
        send_user(call.message)
    elif call.data == 'Рассылка 🆘':
        all_send(call.message)
    else:
        bot.answer_callback_query(call.id, text='Команда в разработке!')


alive.keep_alive()
bot.polling(none_stop=True, interval=0)
