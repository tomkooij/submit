export PATH=$HOME/miniconda/bin:$PATH
export FLASK_APP=submit.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 >>server.log 2>&1
