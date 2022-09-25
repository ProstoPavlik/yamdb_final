import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(os.getcwd(), 'static', 'data', 'review.csv')
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(path, 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(
                i['id'],
                i['title_id'],
                i['text'],
                i['author'],
                i['score'],
                i['pub_date']) for i in dr]
        cur.executemany(
            (f'{"INSERT INTO reviews_review (id, title_id, "}'
             f'{"text, author_id, score, pub_date) "}'
             f'{"VALUES (?, ?, ?, ?, ?, ?);"}'),
            to_db
        )
        con.commit()
        con.close()
