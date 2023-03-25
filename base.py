from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    battle_result = ""
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """ Запуск игры инициализация переменных """
        self.game_is_running = True
        self.player = player
        self.enemy = enemy

    def _check_players_hp(self):
        """ Проверка здоровья игрока и врага, возвращение результата игры """
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
        elif self.enemy.hp <= 0:
            self.battle_result = "Игрок выиграл битву"
        elif self.player.hp <= 0:
            self.battle_result = "Игрок проиграл битву"

    def _stamina_regeneration(self):
        """ Регенерация здоровья и стамины для игрока и врага за ход """

        self.player.stamina += round(self.STAMINA_PER_ROUND * self.player.unit_class.stamina, 1)
        if self.player.stamina > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.stamina_points

        self.enemy.stamina += round(self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina, 1)
        if self.enemy.stamina > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.stamina_points

    def next_turn(self):
        """ Ход соперника, проверка остатка здоровья, восстановление выносливости """
        self._check_players_hp()
        if self.battle_result:
            self.game_is_running = False
            return self.battle_result

        result = self.enemy.hit(self.player)
        self._stamina_regeneration()

        return result

    def end_game(self):
        """ Обработка кнопки Завершение игры. Обнуляем переменные """

        _instances = {}
        self.battle_result = ""
        self.game_is_running = False

    def player_hit(self):
        """ Обработка кнопки Нанести удар """

        if self.game_is_running:
            result = self.player.hit(self.enemy)
            result += " " + self.next_turn()
            return result
        else:
            return self.battle_result

    def player_use_skill(self):
        """ Обработка кнопки Использовать умение """

        if self.game_is_running:
            result = self.player.use_skill(self.enemy)
            result += " " + self.next_turn()
            return result
        else:
            return self.battle_result
