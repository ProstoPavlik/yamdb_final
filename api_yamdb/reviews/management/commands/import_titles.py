import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(os.getcwd(), 'static', 'data', 'titles.csv')
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(path, 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(
                i['id'],
                i['name'],
                i['year'],
                i['category']) for i in dr]
        cur.executemany(
            (f'{"INSERT INTO reviews_title "}'
             f'{"(id, name, year, category_id) VALUES (?, ?, ?, ?);"}'),
            to_db
        )
        con.commit()
        con.close()
