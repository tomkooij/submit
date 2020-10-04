export PATH=$HOME/miniconda/bin:$PATH
#export FLASK_APP=submit.py
#export FLASK_DEBUG=1
#flask run --host=0.0.0.0 >>server.log 2>&1
gunicorn --bind 0.0.0.0:2083 wsgi:app --certfile fullchain.pem --key privkey.pem --access-logfile /home/tom/submitpo2/gunicorn-access.log

