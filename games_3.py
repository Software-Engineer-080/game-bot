import random


def tails():
    return f'--Вы попали в игру--\n⚠️"Орёл и решка"⚠️\n\n'\
           f'Вы играете против Бота!\n\n'\
           f'Одна игра стоит 4 монеты!'


def verify(call, user):
    if user.money < 4:
        return f'Вы не можете сыграть!\n\n' \
               f'Ваш баланс монет: {user.money}💰\n\n' \
               f'Для игры нужно 4💰\n\n' \
               f'Пополните баланс в профиле!'
    else:
        now = random.randint(0, 1)
        player_choice = call.data
        if player_choice == 'Орёл 🦅':  # 0
            players = 0
            if players == now:
                user.update_wins()
                user.add_money(3)
                return f'Поздравляю, {call.from_user.first_name}!\n\n'\
                       f'Вы выиграли 3 монеты!\n\n'\
                       f'Ваш баланс монет: {user.money}💰'
            else:
                user.deduct_money(4)
                return f'Сожалею, {call.from_user.first_name}!\n\n'\
                       f'Вы проиграли 4 монеты!\n\n'\
                       f'Ваш баланс монет: {user.money}💰'
        elif player_choice == 'Решка 🪙':  # 1
            players = 1
            if players == now:
                user.update_wins()
                user.add_money(3)
                return f'Поздравляю, {call.from_user.first_name}!\n\n'\
                       f'Вы выиграли 3 монеты!\n\n'\
                       f'Ваш баланс монет: {user.money}💰'
            else:
                user.deduct_money(4)
                return f'Сожалею, {call.from_user.first_name}!\n\n'\
                       f'Вы проиграли 4 монеты!\n\n'\
                       f'Ваш баланс монет: {user.money}💰'
