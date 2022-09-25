from django.core.management.base import BaseCommand
import csv
import sqlite3
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(os.getcwd(), 'static', 'data', 'genre.csv')
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(path, 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['id'], i['name'], i['slug']) for i in dr]
        cur.executemany(
            'INSERT INTO reviews_genres (id, name, slug) VALUES (?, ?, ?);',
            to_db
        )
        con.commit()
        con.close()
