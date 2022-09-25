import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(os.getcwd(), 'static', 'data', 'comments.csv')
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(path, 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(
                i['id'],
                i['review_id'],
                i['text'],
                i['author'],
                i['pub_date']) for i in dr]
        cur.executemany(
            (f'{"INSERT INTO reviews_comments(id, review_id, "}'
             f'{"text, author_id, pub_date) VALUES (?, ?, ?, ?, ?);"}'),
            to_db
        )
        con.commit()
        con.close()
