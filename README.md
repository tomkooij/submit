Submit
======

Inlever tooltje voor NLT Inleinding programmeren: github.com:tomkooij/nltprog

Auto-grader: Deze tool haalt ingeleverde opdrachten door checkpy.

Flask App die op pythonanywhere.com draait.


Hoe werkt dit?
--------------

Leerlingen leveren opdrachten in. De bestandsnaam bepaald de opdracht,
zoals `checkpy` dat doet. De bestandsnamen zijn hard-coded in `app/models.py`

Opdrachten (`models.Submission`) komen in de wachtrij.

In een console met de juiste virtualenv:

  python run_checkpy

Dit haalt alle opdrachten uit de wachtrij door checkpy.


Installatie
-----------

 - Maak virtualenv op pythonanywhere

Start een console in de virtualenv:

```
git clone github.com:tomkooij/submit
pip install -r requirements.txt
pip install checkpy
checkpy -d uva/progns
pip install matplotlib  # voor checkpy
```
 - Fix de MySQL config en secret in `config.py`

 - Configuratie op de Webtab van pythonanywhere:

  * source code: /home/tomkooij/submit
  * working dir: /home/tomkooij/submit

/var/www/tomkooij_pythonanywhere_com_wsgi.py
```
import sys

# add your project directory to the sys.path
project_home = u'/home/tomkooij/submit'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from submit import app as application
```

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
