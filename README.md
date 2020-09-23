Submit
======

Inlever tooltje voor NLT Inleinding programmeren: github.com:tomkooij/nltprog

Auto-grader: Deze tool haalt ingeleverde opdrachten door checkpy.

Flask App die eerste op pythonanywhere.com draaide. Draait nu op HTPC.


Hoe werkt dit?
--------------


Leerlingen leveren opdrachten in. De bestandsnaam bepaald de opdracht,
zoals `checkpy` dat doet. De bestandsnamen zijn hard-coded in `app/models.py`

(In de branch `olympiade` staat een versie de werkt voor PO1. Hier bepaald
een dropdown menu de opdracht. `run_checkpy` past sowieso de opdrachtnaam
weer opnieuw aan voor `checkpy`)

Opdrachten (`models.Submission`) komen in de wachtrij.


Installatie
-----------

 - Verander de MySQL config (root password) en secret in `config.py`

 - MySQL en checkpy draaien in docker, zie `docker-compose.yml`:
 
 $ docker-compose up -d 

Voeg gebruikers toe:

 - Gebruik `add_users.py` om gebruikers te maken:

xxxx, llnnummber(4cijfers), wachtwoord, Naam, email

  - Maak de admin user:

```python
>>> from app import db
>>> from app.models import User
>>> u = User('tom', 'Tom Kooij', 'foo@foo')
>>> u.set_password(vulietsin)
>>> u.is_admin = True
>>> db.session.add(u)
>>> db.session.commit()
```

Draai de webserver app met `run_flash.sh` in een screen. 

Installeer checkpy ook lokaal en installeer tests in ./tests
(Clone ze van github en kopieer naar `./tests`)
```
pip install checkpy
git checkout git@github.com:tomkooij/io_tests.git (private!)
git checkout git@github.com:Jelleas/progbeta2017tests
cp -R blabla tests/
checkpy -register ./tests
checkpy testietsomtekijkenofhetwerkt.py
```

In de checkpy docker container:

  `$ ./run_checkpy_docker.sh`
(detach met ctrl-p ctrl-q ;) )

Dit haalt alle opdrachten uit de wachtrij door checkpy.
De opdrachten draaien in de checkpy container: chroot jail, submit folder is
read-only gemount. Unpriviledged user. Container geen netwerk toegang.

TODO: 
  - gunicorn (TLS) in plaats van Flask dev server gebruiken
  - timeout in checkpy (infinite loops) debuggen: lijkt niet te werken
