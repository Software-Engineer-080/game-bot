import random


def tails():
    return f'--Вы попали в игру--\n⚠️"Орёл и решка"⚠️\n\n'\
           f'Вы играете против Бота!\n\n'\
           f'Одна игра стоит 4 монеты!'


def verify(message, user):
    if user.money < 4:
        return f'Вы не можете сыграть!\n' \
               f'Ваш баланс монет: {user.money}💰\n' \
               f'Для игры нужно 4💰\n' \
               f'Пополните баланс в профиле!'
    else:
        now = random.randint(0, 1)
        if message.text == 'Орёл 🦅':  # 0
            players = 0
            if players == now:
                user.add_money(3)
                return f'Поздравляю, {message.from_user.first_name}!\n'\
                       f'Вы выиграли 3 монеты!\n'\
                       f'Ваш баланс монет: {user.money}💰'
            else:
                user.deduct_money(4)
                return f'Сожалею, {message.from_user.first_name}!\n'\
                       f'Вы проиграли 4 монеты!\n'\
                       f'Ваш баланс монет: {user.money}💰'
        elif message.text == 'Решка 🪙':  # 1
            players = 1
            if players == now:
                user.add_money(3)
                return f'Поздравляю, {message.from_user.first_name}!\n'\
                       f'Вы выиграли 3 монеты!\n'\
                       f'Ваш баланс монет: {user.money}💰'
            else:
                user.deduct_money(4)
                return f'Сожалею, {message.from_user.first_name}!\n'\
                       f'Вы проиграли 4 монеты!\n'\
                       f'Ваш баланс монет: {user.money}💰'
