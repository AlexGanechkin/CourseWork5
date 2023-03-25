from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass, WarriorClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = Weapon
        self.armor = Armor
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:

        damage = round(self.weapon.damage * self.unit_class.attack, 1)  # расчет урона игрока
        defense = round(target.armor.defence * target.unit_class.armor, 1)  # расчет брони цели

        self.stamina -= self.weapon.stamina_per_hit  # уменьшение выносливости атакующего при ударе

        if target.stamina >= target.armor.stamina_per_turn:
            target.stamina -= target.armor.stamina_per_turn  # уменьшение выносливости защищающегося при использовании брони
        else:
            defense = 0  # если у защищающегося нехватает выносливости - его броня игнорируется

        if damage >= defense:
            damage -= defense
            damage = round(damage, 1)
        else:
            damage = 0

        target.get_damage(damage)

        return damage

    def get_damage(self, damage: float) -> Optional[float]:
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """ метод использования умения. Если умение уже использовано возвращаем строку """

        if not self._is_skill_used:
            return self.unit_class.skill.use(user=self, target=target)
        else:
            return "Навык уже использован."


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """ Функция удар игрока: проверка выносливости, расчет финального уровня повреждения """
        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """ Cоперник наносит удар или с 10% шансом применяет умение (1 раз за бой) """

        if not self._is_skill_used and randint(1, 10) == 5:
            return self.use_skill(target)

        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
