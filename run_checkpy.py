import subprocess
import json
import re
import os, shutil, tempfile

from app import app, db
from app.models import User, Submission, opdracht_score


UPLOAD_PATH = 'uploads'
basedir = os.path.abspath(os.path.dirname(__file__))

def get_uploads_path():
    return os.path.join(basedir, UPLOAD_PATH)

def run_checkpy(path, filename):
    """run `checkpy` in json mode. Return results as string"""
    try:
        return subprocess.run(['checkpy', filename, '--json'], cwd=path, stdout=subprocess.PIPE).stdout
    except Exception as e:
        return str(e)

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


app.app_context().push()

subs = get_ungraded_submissions()

print(15*'#')
print('len(queue) =', len(subs) )
print(15*'#')

for sub in subs:
    fn = os.path.join(get_uploads_path(), sub.submission_filename)
    print(30*"*")
    print('processing {} volgnummer: {}'.format(fn, sub.id))
    print('DEBUG: ', sub)
    print('DEBUG: ', User.query.filter_by(id=sub.user_id).first())
    if not os.path.exists(fn):
        print('skipping {}: Not found.'.format(fn))
        continue
    else:
        with tempfile.TemporaryDirectory() as tmpdirname:
            base, suffix = os.path.splitext(fn)
            new_fn = os.path.join(tmpdirname, sub.category + suffix)
            print(new_fn, sub.category)
            shutil.copy(fn, new_fn)
            checkpy_result = run_checkpy(tmpdirname, sub.category)
            try:
                results = json.loads(checkpy_result.decode())
                if isinstance(results, list):
                    results = results[0]
                nTests = results['nRun']  # the number of actual tests
                nPassed = results['nPassed']
                output = remove_ansi_escape('\n'.join(results['output']))
            except Exception as e:
                print('JSON error: ', e)
                nTests = 0
                nPassed = 0
                output = 'Checkpy error'
            if nTests:
                percentage = nPassed/nTests * 100
                max_score = opdracht_score.get(sub.category, None)
                if max_score is not None:
                    score = int(nPassed/nTests * max_score)
                    print('Max score is: {}'.format(max_score))
            else:
                percentage = 0
                score = 0
            print('In totaal {} tests uitgevoerd. Het percentage is: {}'.format(nTests, percentage))
            print('Score: {}'.format(score))
            print(output)
            sub.percentage = percentage
            sub.score = score
            sub.checkpy_output = output[:999]
            sub.nTests = nTests
            sub.nPassed = nPassed
            sub.is_graded = True
            db.session.commit()
