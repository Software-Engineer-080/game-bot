import random


def stone_game():
    return f'"Камень, Ножницы, Бумага"\n\n'\
           f'Игра говорит сама за себя!\n'\
           f'Стоимость игры 2 монеты!\n\n'\
           f'✊🏻+✋🏻-> ✋🏻 = 8💰\n'\
           f'✋🏻+✌🏻-> ✌🏻 = 8💰\n'\
           f'✌🏻+✊🏻-> ✊🏻 = 8💰'


def stone(user):
    if user.money < 2:
        return f'Вы не можете сыграть!\n' \
               f'Ваш баланс монет: {user.money}💰\n' \
               f'Для игры нужно 2💰\n' \
               f'Пополните баланс в профиле!'
    else:
        user.deduct_money(2)
        bots = random.randint(1, 3)

        if bots == 1:
            bots = '✊🏻'
        elif bots == 2:
            bots = '✌🏻'
        else:
            bots = '✋🏻'

        if '✊🏻' == bots:
            user.add_money(2)
            return f'Ничья!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✊🏻+ {bots} -> ✊🏻✊🏻'\
                   f'Ваш баланс монет: {user.money}💰'

        elif bots == '✌🏻':
            user.add_money(8)
            return f'Вы выиграли 8 монет!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✊🏻+ {bots} -> ✊🏻'\
                   f'Ваш баланс монет: {user.money}💰'

        elif bots == '✋🏻':
            return f'Вы проиграли 2 монеты!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✊🏻+ {bots} -> {bots}'\
                   f'Ваш баланс монет: {user.money}💰'


def scissors(user):
    if user.money < 2:
        return f'Вы не можете сыграть!\n' \
               f'Ваш баланс монет: {user.money}💰\n' \
               f'Для игры нужно 2💰\n' \
               f'Пополните баланс в профиле!'
    else:
        user.deduct_money(2)
        bots = random.randint(1, 3)

        if bots == 1:
            bots = '✊🏻'
        elif bots == 2:
            bots = '✌🏻'
        else:
            bots = '✋🏻'

        if bots == '✊🏻':
            return f'Вы проиграли 2 монеты!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✌🏻+ {bots} -> {bots}'\
                   f'Ваш баланс монет: {user.money}💰'

        elif bots == '✌🏻':
            user.add_money(2)
            return f'Ничья!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✌🏻+ {bots} -> ✌🏻✌🏻'\
                   f'Ваш баланс монет: {user.money}💰'

        elif bots == '✋🏻':
            user.add_money(8)
            return f'Вы выиграли 8 монет!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✌🏻+ {bots} -> ✌🏻'\
                   f'Ваш баланс монет: {user.money}💰'


def paper(user):
    if user.money < 2:
        return f'Вы не можете сыграть!\n' \
               f'Ваш баланс монет: {user.money}💰\n' \
               f'Для игры нужно 2💰\n' \
               f'Пополните баланс в профиле!'
    else:
        user.deduct_money(2)
        bots = random.randint(1, 3)

        if bots == 1:
            bots = '✊🏻'
        elif bots == 2:
            bots = '✌🏻'
        else:
            bots = '✋🏻'

        if bots == '✊🏻':
            user.add_money(8)
            return f'Вы выиграли 8 монет!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✋🏻+ {bots} -> ✋🏻'\
                   f'Ваш баланс монет: {user.money}💰'

        elif bots == '✌🏻':
            return f'Вы проиграли 2 монеты!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✋🏻+ {bots} -> {bots}'\
                   f'Ваш баланс монет: {user.money}💰'

        elif bots == '✋🏻':
            user.add_money(2)
            return f'Ничья!\n'\
                   f'Компьютер выбросил {bots}\n'\
                   f'Получилось: ✋🏻+ {bots} -> ✋🏻✋🏻'\
                   f'Ваш баланс монет: {user.money}💰'
