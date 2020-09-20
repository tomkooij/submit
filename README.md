Submit
======

Inlever tooltje voor NLT Inleinding programmeren: github.com:tomkooij/nltprog

Auto-grader: Deze tool haalt ingeleverde opdrachten door checkpy.

Flask App die eerste op pythonanywhere.com draaide. Draait nu op HTPC.


Hoe werkt dit?
--------------

Draai de app met `run_flash.sh`.

Leerlingen leveren opdrachten in. De bestandsnaam bepaald de opdracht,
zoals `checkpy` dat doet. De bestandsnamen zijn hard-coded in `app/models.py`

(In de branch `olympiade` staat een versie de werkt voor PO1. Hier bepaald
een dropdown menu de opdracht. `run_checkpy` past sowieso de opdrachtnaam
weer opnieuw aan voor `checkpy`)

Opdrachten (`models.Submission`) komen in de wachtrij.

In een screen met de juiste env (`conda activate flask`):

  $ ./run_checkpy

Dit haalt alle opdrachten uit de wachtrij door checkpy.


Installatie
-----------

```
conda activate flask
git clone github.com:tomkooij/submit
pip install -r requirements.txt
pip install checkpy
checkpy -d uva/progns  # voor PO1 is er private repo met de olympiade oplossingen
pip install matplotlib  # voor checkpy
```

 - Fix de MySQL config en secret in `config.py`

 - MySQL draait in docker, zie `docker-compose.yml`:
 
 $ docker-compose up -d 

Voeg gebruikers toe:

 - Gebruik `add_users.py` om gebruikers te maken:

xxxx, llnnummber(4cijfers), wachtwoord, Naam, email

  - Maak de admin user:

```
python
>>> import config
>>> from app import db
>>> from app.models import User
>>> u = User('tom', 'Tom Kooij', 'foo@foo')
>>> u.set_password(vulietsin)
>>> u.is_admin = True
>>> db.session.add(u)
>>> db.session.commit()
```

```
$ flask run --host 0.0.0.0
```

De admin interface is `/admin`
