import re

from jinja2 import Environment, FileSystemLoader
from yaml import load
import sass


UP_REGEX = re.compile(r"\(([^\|]*)\|([^\)]*)\)")


def bg_img(data):
    if data['type'] == 'curse':
        return '/images/bg_skill_black.png'
    elif data['type'] == 'status':
        return '/images/bg_skill_colorless.png'
    else:
        return f"/images/bg_{data['type']}_{data['color']}.png"


def orb_img(data):
    return f"/images/card_{data['color']}_orb.png"


def banner_img(data):
    if data['rarity'] is None or data['rarity'] == 'starter':
        return '/images/banner_common.png'
    else:
        return f"/images/banner_{data['rarity']}.png"


def frame_img(data):
    if data['rarity'] is None:
        return '/images/frame_attack_common.png'
    if data['rarity'] == 'starter':
        return f"/images/frame_{data['type']}_common.png"
    else:
        return f"/images/frame_{data['type']}_{data['rarity']}.png"


def card_img(data, name):
    name = name.replace("'", '').replace(' ', '_').lower()
    if data['type'] == 'curse':
        return '/images/curse/{name}.png'
    elif data['type'] == 'status':
        return '/images/status/{name}.png'
    else:
        return f"/images/{data['color']}/{data['type']}/{name}.png"


def process_text(cost):
    pass


def process_cost(cost):
    if isinstance(cost, int) or cost == 'X':
        return cost
    else:
        return f"""
            <tspan class="base">{cost[1]}</tspan>
            <tspan class="plus">{cost[3]}</tspan>
        """


env = Environment(trim_blocks=True,
                  lstrip_blocks=True,
                  loader=FileSystemLoader('templates'))
env.filters['bg_img'] = bg_img
env.filters['orb_img'] = orb_img
env.filters['banner_img'] = banner_img
env.filters['frame_img'] = frame_img
env.filters['card_img'] = card_img
env.filters['card_text'] = process_text
env.filters['card_cost'] = process_cost
env.filters['titlecase'] = lambda x: x.title()


with open('cards.yaml') as f:
    cards = load(f)

with open('relics.yaml') as f:
    relics = load(f)

with open('potions.yaml') as f:
    potions = load(f)

with open('enemies.yaml') as f:
    enemies = load(f)

env.get_template('index.html').stream().dump('docs/index.html')
env.get_template('cards.html').stream(cards=cards).dump('docs/cards.html')

sass.compile(dirname=('.', 'docs/css'))
