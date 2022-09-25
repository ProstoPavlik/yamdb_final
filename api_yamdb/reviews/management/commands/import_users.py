from django.core.management.base import BaseCommand

import csv
import os
import sqlite3


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(os.getcwd(), 'static', 'data', 'users.csv')
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(path, 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(
                i['id'],
                i['first_name'],
                i['last_name'],
                i['email'],
                i['username'],
                i['role'],
                i['bio']) for i in dr]
        cur.executemany(
            (f'{"INSERT INTO users_user (id, password, "}'
             f'{"last_login, is_superuser, first_name, "}'
             f'{"last_name, is_staff, is_active, date_joined, "}'
             f'{"email, username, role, bio) VALUES "}'
             f'{"(?, 12345678, False, False, ?, ?, False, "}'
             f'{"False, False, ?, ?, ?, ?);"}'),
            to_db
        )
        con.commit()
        con.close()
