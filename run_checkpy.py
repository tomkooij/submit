import subprocess
import json
import re
import os, shutil, tempfile

from app import db
from app.models import User, Submission

UPLOAD_PATH = 'uploads'
basedir = os.path.abspath(os.path.dirname(__file__))

def get_uploads_path():
    return os.path.join(basedir, UPLOAD_PATH)

def run_checkpy(path, filename):
    """run `checkpy` in json mode. Return results as string"""
    return subprocess.run(['checkpy', filename, '--json'], cwd=path, stdout=subprocess.PIPE).stdout


def remove_ansi_escape(line):
    """
    Remove ANSI escape sequences
    https://stackoverflow.com/questions/14693701/

    """
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


def get_ungraded_submissions():
    """return a list of ungraded submissions"""
    return Submission.query.filter_by(is_graded=False).all()


    nTests = results['nTests']
    nPassed = results['nPassed']
    if nTests:
        print('In totaal {nTests} tests uitgevoerd. Het percentage is: {nPassed/nTests}'.format(nTests=nTests, nPassed=nPassed))
    else:
        print('Error: ', remove_ansi_escape(results['output'][0]))


subs = get_ungraded_submissions()
for sub in subs:
    fn = os.path.join(get_uploads_path(), sub.submission_filename)
    if not os.path.exists(fn):
        print('skipping {}: Not found.'.format(fn))
        continue
    else:
        print('processing {} {}'.format(fn, sub))
        with tempfile.TemporaryDirectory() as tmpdirname:
            base, suffix = os.path.splitext(fn)
            new_fn = os.path.join(tmpdirname, sub.category + suffix)
            print(new_fn)
            shutil.copy(fn, new_fn)
            checkpy_result = run_checkpy(tmpdirname, sub.category)
            results = json.loads(checkpy_result.decode())
            nTests = results['nTests']
            nPassed = results['nPassed']
            output = remove_ansi_escape('\n'.join(results['output']))
            if nTests:
                score = nPassed/nTests * 100
                print('In totaal {} tests uitgevoerd. Het percentage is: {}'.format(nTests, score))
                print(output)
                sub.score = score
                sub.checkpy_output = output
                sub.nTests = nTests
                sub.nPassed = nPassed
                sub.is_graded = True
                db.session.commit()
            else:
                print('Error: ', remove_ansi_escape(results['output'][0]))
