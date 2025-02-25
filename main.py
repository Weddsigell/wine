import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='генерирует index.html')
    parser.add_argument(
        'path_product',
        help=f'Путь к файлу с асортиментом',
        type=Path
    )
    return parser.parse_args()


def get_year_format(years):
    if years % 100 in (range(11, 21)):
        return "лет"
    elif years % 10 in (0, 5, 6, 7, 8, 9):
        return "лет"
    elif years % 10 == 1:
        return "год"
    elif years % 10 in range(2, 5):
        return "года"


def main(args):
    years = datetime.datetime.now().year - 1920

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    cards = pandas.read_excel(args.path_product, na_values=' ', keep_default_na=False).to_dict(orient="records")
    cards.sort(key=itemgetter('Категория'))

    goods = {}
    for category, card in groupby(cards, key=itemgetter('Категория')):
        goods[category] = list(card)

    rendered_page = template.render(
        years=f'{years}{get_year_format(years)}',
        goods=goods
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    args = create_parser()
    main(args)
