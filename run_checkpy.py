import subprocess
import json
import re
import os, shutil, pathlib, tempfile

from app import db
from app.models import User, Submission

UPLOAD_PATH = 'uploads'

def get_uploads_path():
    return pathlib.Path.cwd() / UPLOAD_PATH

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
        print(f'In totaal {nTests} tests uitgevoerd. Het percentage is: {nPassed/nTests}')
    else:
        print('Error: ', remove_ansi_escape(results['output'][0]))


subs = get_ungraded_submissions()
for sub in subs:
    fn = get_uploads_path() / sub.submission_filename
    if not fn.exists():
        print(f'skipping {fn}: Not found.')
        continue
    else:
        print(f'processing {fn} {sub}')
        with tempfile.TemporaryDirectory() as tmpdirname:
            new_fn = os.path.join(tmpdirname, sub.category + fn.suffix)
            print(new_fn)
            shutil.copy(fn, new_fn)
            results = json.loads(run_checkpy(tmpdirname, sub.category))
            nTests = results['nTests']
            nPassed = results['nPassed']
            score = nPassed/nTests * 100
            output = remove_ansi_escape('\n'.join(results['output']))
            if nTests:
                print(f'In totaal {nTests} tests uitgevoerd. Het percentage is: {score}')
                print(output)
                sub.score = score
                sub.output = output
                sub.nTests = nTests
                sub.nPassed = nPassed
                db.session.commit()
            else:
                print('Error: ', remove_ansi_escape(results['output'][0]))
