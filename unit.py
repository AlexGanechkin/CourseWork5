from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass, WarriorClass
from random import randint
from typing import Optional, Type


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name: str = name
        self.unit_class: UnitClass = unit_class
        self.hp: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Weapon
        self.armor: Armor
        self._is_skill_used: bool = False

    @property
    def health_points(self) -> float:
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> str:
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:

        self.stamina -= self.weapon.stamina_per_hit  # уменьшение выносливости атакующего при ударе

        damage = round(self.weapon.damage * self.unit_class.attack, 1)  # расчет урона игрока

        if target.stamina >= target.armor.stamina_per_turn:
            target.stamina -= target.armor.stamina_per_turn  # уменьшение выносливости защищающегося при использовании брони
            damage -= round(target.armor.defence * target.unit_class.armor, 1)
        # если у защищающегося нехватает выносливости - его броня игнорируется
        damage = round(damage, 1)
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: float) -> Optional[float]:
        if damage > 0:
            self.hp -= damage

        if self.hp < 0:
            self.hp = 0
        return self.hp

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """ метод использования умения. Если умение уже использовано возвращаем строку """

        if self._is_skill_used:
            return "Навык уже использован."
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """ Функция удар игрока: проверка выносливости, расчет финального уровня повреждения """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """ Cоперник наносит удар или с 10% шансом применяет умение (1 раз за бой) """

        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 100:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
