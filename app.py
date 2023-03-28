from random import randint

from flask import Flask, render_template, request, redirect, url_for

from base import Arena
from classes import unit_classes
from equipment import EquipmentData, Equipment
from unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": ...,
    "enemy": ...,
}

unit_class = list(unit_classes.keys())
weapons = Equipment().get_weapons_names()
armors = Equipment().get_armors_names()
hero_default_name = ['Святогор', 'Капитан Америка', 'Добрыня Никитич']
enemy_default_name = ['Танос', 'Хан Батый', 'Т-1000']

arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        return render_template('fight.html', heroes=heroes, result=arena.player_hit())
    else:
        return render_template('fight.html', heroes=heroes, battle_result=arena.player_hit())


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        return render_template('fight.html', heroes=heroes, result=arena.player_use_skill())
    else:
        return render_template('fight.html', heroes=heroes, battle_result=arena.player_use_skill())


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        return render_template('fight.html', heroes=heroes, result=arena.next_turn())
    else:
        return render_template('fight.html', heroes=heroes, battle_result=arena.next_turn())


@app.route("/fight/end-fight")
def end_fight():
    arena.end_game()
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == "GET":
        result = {
            "header": "героя",  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": Equipment().get_weapons_names(),  # для названия оружия
            "armors": Equipment().get_armors_names()  # для названия брони
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == "POST":
        hero_name = request.form.get('name')
        hero_class = request.values.get('unit_class')
        hero_weapon = request.form.get('weapon')
        hero_armor = request.form.get('armor')
        if hero_name is None:
            hero_name, hero_class, hero_weapon, hero_armor = choose_default_unit('player')

        player = PlayerUnit(hero_name, unit_class=unit_classes[hero_class])
        player.equip_weapon(Equipment().get_weapon(weapon_name=hero_weapon))
        player.equip_armor(Equipment().get_armor(armor_name=hero_armor))

        heroes['player'] = player
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        result = {
            "header": "противника",  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": Equipment().get_weapons_names(),  # для названия оружия
            "armors": Equipment().get_armors_names()  # для названия брони
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == "POST":
        enemy_name = request.form.get('name')
        enemy_class = request.values.get('unit_class')
        enemy_weapon = request.form.get('weapon')
        enemy_armor = request.form.get('armor')
        if enemy_name is None:
            enemy_name, enemy_class, enemy_weapon, enemy_armor = choose_default_unit('enemy')

        enemy = EnemyUnit(enemy_name, unit_class=unit_classes[enemy_class])
        enemy.equip_weapon(Equipment().get_weapon(weapon_name=enemy_weapon))
        enemy.equip_armor(Equipment().get_armor(armor_name=enemy_armor))

        heroes['enemy'] = enemy
        return redirect(url_for("start_fight"))


def choose_default_unit(unit_type):
    if unit_type == 'player':
        default_unit_name = hero_default_name[randint(0, len(hero_default_name)-1)]
    else:
        default_unit_name = enemy_default_name[randint(0, len(hero_default_name) - 1)]

    default_unit_class = unit_class[randint(0, len(unit_class) - 1)]
    default_weapon = weapons[randint(0, len(weapons) - 1)]
    default_armor = armors[randint(0, len(armors) - 1)]
    return default_unit_name, default_unit_class, default_weapon, default_armor


if __name__ == "__main__":
    app.run()
