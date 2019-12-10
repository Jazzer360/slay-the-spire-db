from jinja2 import Environment, FileSystemLoader
from yaml import load
import sass

env = Environment(trim_blocks=True,
                  lstrip_blocks=True,
                  loader=FileSystemLoader('templates'))

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
