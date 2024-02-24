def dice():
    return f'Бросайте "Кости", Господа!\n\n' \
           f'Одна игра стоит 6 монет!\n\n' \
           f'🎲 < 3 --> 10💰\n' \
           f'🎲 = 3 --> 15💰\n' \
           f'🎲 > 3 --> 10💰\n'


def dice_min(dice_1, user):
    print(dice_1.dice.value)
    if user.money < 6:
        return f'Вы не можете сыграть!\n\n' \
               f'Ваш баланс монет: {user.money}💰\n\n' \
               f'Для игры нужно 6💰\n\n' \
               f'Пополните баланс в профиле!'

    else:
        user.deduct_money(6)
        if dice_1.dice.value < 3:
            user.add_money(10)
            user.update_wins()  # Увеличиваем количество побед
            return f'Вы выиграли 10 монет!\n\n' \
                   f'Выпало: {dice_1.dice.value}\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
        else:
            return f'Вы проиграли 6 монет!\n\n' \
                   f'Выпало: {dice_1.dice.value}\n\n' \
                   f'Ваш баланс монет: {user.money}💰'


def dice_three(dice_2, user):
    print(dice_2.dice.value)
    if user.money < 6:
        return f'Вы не можете сыграть!\n\n' \
               f'Ваш баланс монет: {user.money}💰\n\n' \
               f'Для игры нужно 6💰\n\n' \
               f'Пополните баланс в профиле!'

    else:
        user.deduct_money(6)
        if dice_2.dice.value == 3:
            user.add_money(15)
            user.update_wins()  # Увеличиваем количество побед
            return f'Вы выиграли 15 монет!\n\n' \
                   f'Выпало: {dice_2.dice.value}\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
        else:
            return f'Вы проиграли 6 монет!\n\n' \
                   f'Выпало: {dice_2.dice.value}\n\n' \
                   f'Ваш баланс монет: {user.money}💰'


def dice_max(dice_3, user):
    print(dice_3.dice.value)
    if user.money < 6:
        return f'Вы не можете сыграть!\n\n' \
               f'Ваш баланс монет: {user.money}💰\n\n' \
               f'Для игры нужно 6💰\n\n' \
               f'Пополните баланс в профиле!'

    else:
        user.deduct_money(6)
        if dice_3.dice.value > 3:
            user.add_money(10)
            user.update_wins()  # Увеличиваем количество побед
            return f'Вы выиграли 10 монет!\n\n' \
                   f'Выпало: {dice_3.dice.value}\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
        else:
            return f'Вы проиграли 6 монет!\n\n' \
                   f'Выпало: {dice_3.dice.value}\n\n' \
                   f'Ваш баланс монет: {user.money}💰'
