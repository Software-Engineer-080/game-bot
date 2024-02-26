import random


class BlackjackGame:
    def __init__(self):
        # self.cards = {'J♥️': 2, 'Q♥️': 3, 'K♥️': 4, '6♥️': 6, '7♥️': 7, '8♥️': 8, '9♥️': 9, '10♥️': 10, 'T♥️': 11,
        #               'J♠️': 2, 'Q♠️': 3, 'K♠️': 4, '6♠️': 6, '7♠️': 7, '8♠️': 8, '9♠️': 9, '10♠️': 10, 'T♠️': 11,
        #               'J♦️': 2, 'Q♦️': 3, 'K♦️': 4, '6♦️': 6, '7♦️': 7, '8♦️': 8, '9♦️': 9, '10♦️': 10, 'T♦️': 11,
        #               'J♣️': 2, 'Q♣️': 3, 'K♣️': 4, '6♣️': 6, '7♣️': 7, '8♣️': 8, '9♣️': 9, '10♣️': 10, 'T♣️': 11}

        self.cards = {
            '6♥️': 6, '6♠️': 6, '6♦️': 6, '6♣️': 6,
            '7♥️': 7, '7♠️': 7, '7♦️': 7, '7♣️': 7,
            '8♥️': 8, '8♠️': 8, '8♦️': 8, '8♣️': 8,
            '9♥️': 9, '9♠️': 9, '9♦️': 9, '9♣️': 9,
            '10♥️': 10, '10♠️': 10, '10♦️': 10, '10♣️': 10,
            'J♥️': 2, 'J♠️': 2, 'J♦️': 2, 'J♣️': 2,
            'Q♥️': 3, 'Q♠️': 3, 'Q♦️': 3, 'Q♣️': 3,
            'K♥️': 4, 'K♠️': 4, 'K♦️': 4, 'K♣️': 4,
            'T♥️': 11, 'T♠️': 11, 'T♦️': 11, 'T♣️': 11
        }

        self.gamer_list = []
        self.dealer_list = []
        self.gamer_summ = 0
        self.dealer_summ = 0
        self.amount = 0

    @staticmethod
    def start_card():
        return f"Вас приветствует 'Очко (21)'\n\n" \
               f"Правила смотрите в соответствующем разделе\n\n"

    @staticmethod
    def rules():
        return f"Вы зашли в правила игры '21'\n\n " \
               f"1. Цель игры - набрать комбинацию карт, которая в сумме должна дать 21\n\n" \
               f"2. Цена карт:\n\n" \
               f"   \t6♥️♠️♦️♣️(Шесть) - 6\n" \
               f"   \t7♥️♠️♦️♣️(Семь) - 7\n" \
               f"   \t8♥️♠️♦️♣️(Восемь) - 8\n" \
               f"   \t9♥️♠️♦️♣️(Девять) - 9\n" \
               f"   \t10♥️♠️♦️♣️(Десять) - 10\n" \
               f"   \tJ♥️♠️♦️♣️(Валет) - 2\n" \
               f"   \tQ♥️♠️♦️♣️(Дама) - 3\n" \
               f"   \tK♥️♠️♦️♣️(Король) - 4\n" \
               f"   \tT♥️♠️♦️♣️(Туз) - 11\n\n" \
               f"3. Суть игры:\n\n" \
               f"С начала игры тебе раздаётся 2 карты и показывается их сумма\n\n" \
               f"По необходимости ты можешь добрать карт, нажав на кнопку 'Ещё'\n\n" \
               f"Если у тебя на руках достаточно карт, но не меньше 15, то " \
               f"ты можешь нажать на кнопку 'Стоп', тогда карты начнет набирать Дилер\n\n" \
               f"Чья сумма карт будет ближе всего к 21, но не больше его, тот и победил\n\n" \
               f"‼️ В игре присутствует\n'Золотое Очко'‼️\n\n" \
               f"4. Удача всегда с тобой 🍀"

    def start(self):
        self.gamer_list = []
        self.dealer_list = []
        self.gamer_summ = 0
        self.dealer_summ = 0
        self.amount = 0
        return 'Выберите ставку:'

    def game(self, user, amount):
        if user.money < amount:
            return (f'Вы не можете сыграть!\n\n'
                    f'Ваш баланс монет: {user.money}💰\n\n'
                    f'Для игры нужно {amount}💰\n\n'
                    f'Пополните баланс в профиле!')
        else:
            while len(self.gamer_list) != 2:
                rnd_crd = random.choice(list(self.cards.keys()))
                if rnd_crd not in self.gamer_list:
                    self.gamer_list.append(rnd_crd)
                else:
                    continue
            self.amount += amount
            for i in range(len(self.gamer_list)):
                self.gamer_summ += self.cards[self.gamer_list[i]]
            return (f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                    f'Сумма карт: {self.gamer_summ}')

    def add_card(self):
        if self.gamer_summ < 22:
            if self.gamer_summ == 21:
                return (f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                        f'Сумма карт: {self.gamer_summ}\n\n'
                        f'У вас "Очко"!\n\n'
                        f'Нажмите кнопку "Хватит"!')
            else:
                new_card = random.choice(list(self.cards.keys()))
                while new_card in self.gamer_list:
                    new_card = random.choice(list(self.cards.keys()))
                self.gamer_list.append(new_card)
                self.gamer_summ += self.cards[new_card]
                return (f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                        f'Сумма карт: {self.gamer_summ}')
        elif (self.gamer_summ == 22) and (len(self.gamer_list) == 2):
            return (f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                    f'Сумма карт: {self.gamer_summ}\n\n'
                    f'У вас "Золотое Очко"!\n\n'
                    f'Нажмите кнопку "Хватит"!')
        else:
            return (f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                    f'Сумма карт: {self.gamer_summ}\n\n'
                    f'У вас перебор!\n\n'
                    f'Нажмите кнопку "Хватит"!')

    def stop_card(self, user):
        while True:
            if self.dealer_summ < 16:
                new_card = random.choice(list(self.cards.keys()))
                if (new_card not in self.gamer_list) and (new_card not in self.dealer_list):
                    self.dealer_list.append(new_card)
                    self.dealer_summ += self.cards[new_card]
                else:
                    continue
            else:
                print('Сумма Дилера:', self.dealer_summ)
                print('Сумма Игрока:', self.gamer_summ)
                print()

                if (((len(self.dealer_list) == 2) and (self.dealer_summ == 22))
                        and ((len(self.gamer_list) != 2) or (self.gamer_summ != 22))):

                    user.deduct_money(self.amount)
                    return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                            f'Сумма карт: {self.dealer_summ}\n\n\n'
                            f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                            f'Сумма карт: {self.gamer_summ}\n\n\n'
                            f'У Дилера "Золотое Очко"!\n\n'
                            f'Побеждает Дилер!\nВы проиграли {self.amount}💰\n\n'
                            f'Ваш баланс монет: {user.money}💰')

                elif (((len(self.dealer_list) != 2) or (self.dealer_summ != 22))
                      and ((len(self.gamer_list) == 2) and (self.gamer_summ == 22))):

                    user.update_wins()
                    user.add_money(self.amount)
                    return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                            f'Сумма карт: {self.dealer_summ}\n\n\n'
                            f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                            f'Сумма карт: {self.gamer_summ}\n\n\n'
                            f'У Вас "Золотое Очко"!\n\n'
                            f'Вы выиграли {self.amount}💰\n\n'
                            f'Ваш баланс монет: {user.money}💰')

                elif (((len(self.dealer_list) == 2) and (self.dealer_summ == 22))
                      and ((len(self.gamer_list) == 2) and (self.gamer_summ == 22))):

                    return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                            f'Сумма карт: {self.dealer_summ}\n\n\n'
                            f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                            f'Сумма карт: {self.gamer_summ}\n\n\n'
                            f'У вас у обоих "Золотое Очко"!\n\n'
                            f'Ничья! Ваш баланс: {user.money}💰')

                elif (
                        (
                                ((self.dealer_summ >= 16) and (self.dealer_summ <= 21)) and
                                ((self.gamer_summ >= 15) and (self.gamer_summ <= 21))
                        )
                ):

                    if self.dealer_summ > self.gamer_summ:

                        user.deduct_money(self.amount)
                        return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                                f'Сумма карт: {self.dealer_summ}\n\n\n'
                                f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                                f'Сумма карт: {self.gamer_summ}\n\n\n'
                                f'Побеждает Дилер!\nВы проиграли {self.amount}💰\n\n'
                                f'Ваш баланс монет: {user.money}💰')

                    elif self.dealer_summ < self.gamer_summ:

                        user.update_wins()
                        user.add_money(self.amount)
                        return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                                f'Сумма карт: {self.dealer_summ}\n\n\n'
                                f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                                f'Сумма карт: {self.gamer_summ}\n\n\n'
                                f'Вы выиграли {self.amount}💰\n\n'
                                f'Ваш баланс монет: {user.money}💰')

                    elif self.dealer_summ == self.gamer_summ:

                        return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                                f'Сумма карт: {self.dealer_summ}\n\n\n'
                                f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                                f'Сумма карт: {self.gamer_summ}\n\n\n'
                                f'Ничья! Ваш баланс: {user.money}💰')

                elif (((self.dealer_summ >= 16) and (self.dealer_summ <= 21)) and
                      ((self.gamer_summ < 15) or (self.gamer_summ > 21))):

                    if self.gamer_summ > 21:

                        user.deduct_money(self.amount)
                        return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                                f'Сумма карт: {self.dealer_summ}\n\n\n'
                                f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                                f'Сумма карт: {self.gamer_summ}\n\n\n'
                                f'У Вас перебор!\nПобеждает Дилер!\n'
                                f'Вы проиграли {self.amount}💰\n\n'
                                f'Ваш баланс монет: {user.money}💰')

                    elif self.gamer_summ < 15:

                        user.deduct_money(self.amount)
                        return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                                f'Сумма карт: {self.dealer_summ}\n\n\n'
                                f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                                f'Сумма карт: {self.gamer_summ}\n\n\n'
                                f'У Вас недобор!\nПобеждает Дилер!\n'
                                f'Вы проиграли {self.amount}💰\n\n'
                                f'Ваш баланс монет: {user.money}💰')

                elif (((self.dealer_summ < 16) or (self.dealer_summ > 21)) and
                      ((self.gamer_summ < 15) or (self.gamer_summ > 21))):

                    return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                            f'Сумма карт: {self.dealer_summ}\n\n\n'
                            f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                            f'Сумма карт: {self.gamer_summ}\n\n\n'
                            f'Вы оба проиграли!\n\n'
                            f'Ваш баланс: {user.money}💰')

                elif (((self.dealer_summ < 16) or (self.dealer_summ > 21)) and
                      ((self.gamer_summ >= 15) and (self.gamer_summ <= 21))):

                    user.update_wins()
                    user.add_money(self.amount)
                    return (f'Сейчас на руках у Дилера:\n{self.dealer_list}\n\n'
                            f'Сумма карт: {self.dealer_summ}\n\n\n'
                            f'Сейчас у Вас на руках:\n{self.gamer_list}\n\n'
                            f'Сумма карт: {self.gamer_summ}\n\n\n'
                            f'Вы выиграли {self.amount}💰\n\n'
                            f'Ваш баланс монет: {user.money}💰')

                else:
                    return 'Ошибка! Свяжитесь с разработчиком!'
