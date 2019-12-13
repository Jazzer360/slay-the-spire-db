import re

from jinja2 import Environment, FileSystemLoader
import yaml
import sass

with open('cards.yaml') as f:
    cards = yaml.load(f, Loader=yaml.FullLoader)

with open('relics.yaml') as f:
    relics = yaml.load(f, Loader=yaml.FullLoader)

with open('potions.yaml') as f:
    potions = yaml.load(f, Loader=yaml.FullLoader)

with open('enemies.yaml') as f:
    enemies = yaml.load(f, Loader=yaml.FullLoader)

with open('keywords.yaml') as f:
    keywords = yaml.load(f, Loader=yaml.FullLoader)

UP_REGEX = re.compile(r"(\([^\|]*\|[^\)]*\))")
UP_REGEX_SPLIT = re.compile(r"\(([^\|]*)\|([^\)]*)\)")
KW_REGEX = re.compile('|'.join(keywords))


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


def process_card_text(text, color):
    text = text.replace('\n', '<br>')
    output = ''
    for segment in UP_REGEX.split(text):
        match = UP_REGEX_SPLIT.search(segment)
        if match:
            output += env.get_template('card-text-plus.html').render(
                base=match[1], plus=match[2])
        else:
            output += segment
    output = output.replace(
        '[orb]',
        env.get_template('card-text-orb.html').render(color=color))
    output = KW_REGEX.sub(kw_replace, output)
    return output


def process_card_cost(cost):
    if isinstance(cost, int) or cost == 'X':
        return cost
    else:
        return env.get_template('card-text-cost.html').render(
            basecost=cost[1], pluscost=cost[3])


def kw_replace(match):
    return env.get_template('card-text-keyword.html').render(keyword=match[0])


env = Environment(trim_blocks=True,
                  lstrip_blocks=True,
                  loader=FileSystemLoader('templates'))
env.filters['bg_img'] = bg_img
env.filters['orb_img'] = orb_img
env.filters['banner_img'] = banner_img
env.filters['frame_img'] = frame_img
env.filters['card_img'] = card_img
env.filters['card_text'] = process_card_text
env.filters['card_cost'] = process_card_cost
env.filters['titlecase'] = lambda x: x.title()

env.get_template('index.html').stream().dump('docs/index.html')
env.get_template('cards.html').stream(cards=cards).dump('docs/cards.html')

sass.compile(dirname=('.', 'docs/css'))
