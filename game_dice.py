def dice():
    return f'Бросайте "Кости", Господа!\n\n' \
           f'Одна игра стоит 4 монеты!\n\n' \
           f'🎲 < 3 --> 8💰\n' \
           f'🎲 = 3 --> 13💰\n' \
           f'🎲 > 3 --> 8💰\n'


def dice_min(dice_1, user):
    print(f'У {user.name} - {user.id} выпала кость:', dice_1.dice.value)
    user.deduct_money(4)
    if dice_1.dice.value < 3:
        user.add_money(8)
        user.update_wins()
        return f'Вы выиграли 8 монет!\n\n' \
               f'Выпало: {dice_1.dice.value}\n\n' \
               f'Ваш баланс монет: {user.money}💰'
    else:
        return f'Вы проиграли 4 монеты!\n\n' \
               f'Выпало: {dice_1.dice.value}\n\n' \
               f'Ваш баланс монет: {user.money}💰'


def dice_three(dice_2, user):
    print(f'У {user.name} - {user.id} выпала кость:', dice_2.dice.value)
    user.deduct_money(4)
    if dice_2.dice.value == 3:
        user.add_money(13)
        user.update_wins()
        return f'Вы выиграли 13 монет!\n\n' \
               f'Выпало: {dice_2.dice.value}\n\n' \
               f'Ваш баланс монет: {user.money}💰'
    else:
        return f'Вы проиграли 4 монеты!\n\n' \
               f'Выпало: {dice_2.dice.value}\n\n' \
               f'Ваш баланс монет: {user.money}💰'


def dice_max(dice_3, user):
    print(f'У {user.name} - {user.id} выпала кость:', dice_3.dice.value)
    user.deduct_money(4)
    if dice_3.dice.value > 3:
        user.add_money(8)
        user.update_wins()
        return f'Вы выиграли 8 монет!\n\n' \
               f'Выпало: {dice_3.dice.value}\n\n' \
               f'Ваш баланс монет: {user.money}💰'
    else:
        return f'Вы проиграли 4 монеты!\n\n' \
               f'Выпало: {dice_3.dice.value}\n\n' \
               f'Ваш баланс монет: {user.money}💰'
