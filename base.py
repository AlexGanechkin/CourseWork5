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
    battle_result = None
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """ Запуск игры инициализация переменных """
        self.game_is_running = True
        self.player = player
        self.enemy = enemy

    def _check_players_hp(self) -> None:
        """ Проверка здоровья игрока и врага, возвращение результата игры """
        if self.player.hp > 0 and self.enemy.hp > 0:  # от наставника
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
        elif self.enemy.hp <= 0:
            self.battle_result = "Игрок выиграл битву"
        elif self.player.hp <= 0:
            self.battle_result = "Игрок проиграл битву"

        # return self.end_game() - от наставника

    def _stamina_regeneration(self) -> None:
        """ Регенерация здоровья и стамины для игрока и врага за ход """

        units = (self.player, self.enemy)

        for unit in units:
            unit.stamina += round(self.STAMINA_PER_ROUND * unit.unit_class.stamina, 1)
            if unit.stamina > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina

    def next_turn(self) -> str:
        """ Ход соперника, проверка остатка здоровья, восстановление выносливости """
        self._check_players_hp()
        if self.battle_result:
            self.game_is_running = False
            return self.battle_result

        self._stamina_regeneration()

        return self.enemy.hit(self.player)

    def end_game(self) -> None:
        """ Обработка кнопки Завершение игры. Обнуляем переменные """

        self._instances = {}
        self.battle_result = ""
        self.game_is_running = False
        # return self.battle_result - от наставника

    def player_hit(self) -> str:
        """ Обработка кнопки Нанести удар """

        if self.game_is_running:
            result = self.player.hit(self.enemy)
            turn_result = self.next_turn()
            return f"{result}<br>{turn_result}"
        else:
            return self.battle_result

    def player_use_skill(self) -> str:
        """ Обработка кнопки Использовать умение """

        if self.game_is_running:
            result = self.player.use_skill(self.enemy)
            turn_result = self.next_turn()
            return f"{result}<br>{turn_result}"
        else:
            return self.battle_result
