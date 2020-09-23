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
MySQL en checkpy daaien in Docker containers: `docker-compose up -d`.

Draai de webserver app met `run_flash.sh`. TODO: gunicorn ervoor zetten (TLS).

In de checkpy docker container:
  $ ./run_checkpy_docker.sh
(detach met ctrl-p ctrl-q ;) )

Dit haalt alle opdrachten uit de wachtrij door checkpy.
De opdrachten draaien de checkpy container: chroot jail, submit folder is
read-only gemount. Unpriviledge user.

TODO: 
  - checkpy container beter firewallen
  - timeout in checkpy (infinite loops) debuggen: lijkt niet te werken


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
