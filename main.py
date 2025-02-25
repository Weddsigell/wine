import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from itertools import groupby
from operator import itemgetter
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


def get_age():
    years = datetime.datetime.now().year - 1920
    return f'{years} {get_year_format(years)}'


def get_year_format(years):
    if years % 100 in (range(11, 21)):
        return "лет"
    elif years % 10 in (0, 5, 6, 7, 8, 9):
        return "лет"
    elif years % 10 == 1:
        return "год"
    elif years % 10 in range(2, 5):
        return "года"


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

cards = pandas.read_excel('wine3.xlsx', na_values=' ', keep_default_na=False).to_dict(orient="records")
cards.sort(key=itemgetter('Категория'))
goods = {}

for key, val in groupby(cards, key=itemgetter('Категория')):
    goods[key] = list(val)

rendered_page = template.render(
    years=get_age(),
    goods=goods
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
