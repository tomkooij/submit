import csv, random

from app import db
from app.models import User, Submission


SOM_EXPORT = 'users.csv'

def generate_password(length):
    pw_set = ('abcdefghijkmnpqrstuvwxyz'
                '23456789')
    pw = length * ' '
    return ''.join([random.choice(pw_set) for c in pw])

with open(SOM_EXPORT, 'r') as csvfile:
    r = csv.reader(csvfile, delimiter=';')
    with open('passwd.csv', 'w') as outfile:
        w = csv.writer(outfile,  dialect='excel')
        w.writerow(['id', 'username', 'ww', 'naam'])

        users = []
        for row in r:
            #print(row)
            _, llnnummer, naam, *rest = row
            assert int(llnnummer)
            username = 'cg'+llnnummer
            password = generate_password(6)
            print(username, password, naam)
            u = User.query.filter_by(username=username).first()
            if u is not None:
                print('User found!', u)
            else:
                u = User(username, naam)
                print('New user: ', u)
            u.set_password(password)
            u.naam = naam
            db.session.add(u)
            w.writerow([u.id, username, password, naam])
        db.session.commit()
