import random


def casino():
    return f'Вас приветствует игра\n"Однорукий Бандит"\n\n' \
           f'Одна игра стоит 5 монет!\n\n' \
           f'💎-💎-💎 = 50💰\n' \
           f'🧨-🧨-🧨 = 30💰\n' \
           f'🕹️-🕹️-🕹️ = 15💰\n' \
           f'💥-💥-💥 = 5💰'


def casino_fire(user):
    if user.money < 5:
        return f'Вы не можете сыграть!\n\n' \
               f'Ваш баланс монет: {user.money}💰\n\n' \
               f'Для игры нужно 5💰\n\n' \
               f'Пополните баланс в профиле!'
    else:
        user.deduct_money(5)
        one = random.randint(1, 4)
        two = random.randint(1, 4)
        three = random.randint(1, 4)

        if one == 1:
            one = '💎'
        elif one == 2:
            one = '🧨'
        elif one == 3:
            one = '🕹'
        else:
            one = '💥'

        if two == 1:
            two = '💎'
        elif two == 2:
            two = '🧨'
        elif two == 3:
            two = '🕹'
        else:
            two = '💥'

        if three == 1:
            three = '💎'
        elif three == 2:
            three = '🧨'
        elif three == 3:
            three = '🕹'
        else:
            three = '💥'

        if one == two == three == '💎':
            user.update_wins()
            user.add_money(50)
            return f'Вы выиграли 50 монет!\n\n' \
                   f'Выпало: {one}-{two}-{three}\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
        elif one == two == three == '🧨':
            user.update_wins()
            user.add_money(30)
            return f'Вы выиграли 30 монет!\n\n' \
                   f'Выпало: {one}-{two}-{three}\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
        elif one == two == three == '🕹':
            user.update_wins()
            user.add_money(15)
            return f'Вы выиграли 15 монет!\n\n'\
                   f'Выпало: {one}-{two}-{three}\n\n'\
                   f'Ваш баланс монет: {user.money}💰'
        elif one == two == three == '💥':
            user.update_wins()
            user.add_money(5)
            return f'Вы выиграли 5 монет!\n\n'\
                   f'Выпало: {one}-{two}-{three}\n\n'\
                   f'Ваш баланс монет: {user.money}💰'
        else:
            return f'Вы проиграли 5 монет!\n\n'\
                   f'Выпало: {one}-{two}-{three}\n\n'\
                   f'Ваш баланс монет: {user.money}💰'
