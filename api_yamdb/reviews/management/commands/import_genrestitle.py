from django.core.management.base import BaseCommand

import os
import sqlite3
import csv


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(os.getcwd(), 'static', 'data', 'genre_title.csv')
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(path, 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['id'], i['title_id'], i['genre_id']) for i in dr]
        cur.executemany(
            (f'{"INSERT INTO reviews_genrestitle "}'
             f'{"(id, genre_id, title_id) VALUES (?, ?, ?);"}'),
            to_db
        )
        con.commit()
        con.close()
