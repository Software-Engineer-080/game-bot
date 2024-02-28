import random


def stone_game():
    return f'"Камень, Ножницы, Бумага"\n\n' \
           f'Игра говорит сама за себя!\n\n' \
           f'Стоимость игры 2 монеты!\n\n' \
           f'✊🏻+✋🏻-> ✋🏻 = 3💰\n' \
           f'✋🏻+✌🏻-> ✌🏻 = 3💰\n' \
           f'✌🏻+✊🏻-> ✊🏻 = 3💰'


def stone(user):
    user.deduct_money(2)
    bots = random.randint(1, 3)

    if bots == 1:
        bots = '✊🏻'
    elif bots == 2:
        bots = '✌🏻'
    else:
        bots = '✋🏻'

    if '✊🏻' == bots:
        user.update_wins()
        user.add_money(2)
        return f'Ничья!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✊🏻+ {bots} -> ✊🏻✊🏻\n\n' \
               f'Ваш баланс монет: {user.money}💰'

    elif bots == '✌🏻':
        user.update_wins()
        user.add_money(3)
        return f'Вы выиграли 3 монеты!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✊🏻+ {bots} -> ✊🏻\n\n' \
               f'Ваш баланс монет: {user.money}💰'

    elif bots == '✋🏻':
        return f'Вы проиграли 2 монеты!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✊🏻+ {bots} -> {bots}\n\n' \
               f'Ваш баланс монет: {user.money}💰'


def scissors(user):
    user.deduct_money(2)
    bots = random.randint(1, 3)

    if bots == 1:
        bots = '✊🏻'
    elif bots == 2:
        bots = '✌🏻'
    else:
        bots = '✋🏻'

    if bots == '✊🏻':
        return f'Вы проиграли 2 монеты!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✌🏻+ {bots} -> {bots}\n\n' \
               f'Ваш баланс монет: {user.money}💰'

    elif bots == '✌🏻':
        user.update_wins()
        user.add_money(2)
        return f'Ничья!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✌🏻+ {bots} -> ✌🏻✌🏻\n\n' \
               f'Ваш баланс монет: {user.money}💰'

    elif bots == '✋🏻':
        user.update_wins()
        user.add_money(3)
        return f'Вы выиграли 3 монеты!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✌🏻+ {bots} -> ✌🏻\n\n' \
               f'Ваш баланс монет: {user.money}💰'


def paper(user):
    user.deduct_money(2)
    bots = random.randint(1, 3)

    if bots == 1:
        bots = '✊🏻'
    elif bots == 2:
        bots = '✌🏻'
    else:
        bots = '✋🏻'

    if bots == '✊🏻':
        user.update_wins()
        user.add_money(3)
        return f'Вы выиграли 3 монеты!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✋🏻+ {bots} -> ✋🏻\n\n' \
               f'Ваш баланс монет: {user.money}💰'

    elif bots == '✌🏻':
        return f'Вы проиграли 2 монеты!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✋🏻+ {bots} -> {bots}\n\n' \
               f'Ваш баланс монет: {user.money}💰'

    elif bots == '✋🏻':
        user.update_wins()
        user.add_money(2)
        return f'Ничья!\n\n' \
               f'Компьютер выбросил {bots}\n\n' \
               f'Получилось: ✋🏻+ {bots} -> ✋🏻✋🏻\n\n' \
               f'Ваш баланс монет: {user.money}💰'
