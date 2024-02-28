import random


def tails():
    return f'--Вы попали в игру--\n⚠️"Орёл и решка"⚠️\n\n' \
           f'Вы играете против Бота!\n\n' \
           f'Одна игра стоит 3 монеты!'


def verify(call, user):
    now = random.randint(0, 1)
    player_choice = call.data
    if player_choice == 'Орёл 🦅':  # 0
        players = 0
        if players == now:
            user.update_wins()
            user.add_money(3)
            return f'Поздравляю, {call.from_user.first_name}!\n\n' \
                   f'Вы выиграли 3 монеты!\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
        else:
            user.deduct_money(3)
            return f'Сожалею, {call.from_user.first_name}!\n\n' \
                   f'Вы проиграли 3 монеты!\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
    elif player_choice == 'Решка 🪙':  # 1
        players = 1
        if players == now:
            user.update_wins()
            user.add_money(3)
            return f'Поздравляю, {call.from_user.first_name}!\n\n' \
                   f'Вы выиграли 3 монеты!\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
        else:
            user.deduct_money(3)
            return f'Сожалею, {call.from_user.first_name}!\n\n' \
                   f'Вы проиграли 3 монеты!\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
