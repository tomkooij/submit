from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db, pycode
from app.models import User, Submission, categories
from app.forms import LoginForm, SubmissionForm


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SubmissionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            fn = form.submission_file.data.filename
            cat = fn.split('.', 1)[0]
            if cat in categories:
                filename = pycode.save(form.submission_file.data, folder=secure_filename(current_user.username))
                new_submission = Submission(filename=filename, comment=str(form.comment.data), user_id=current_user.id, category=cat)
                db.session.add(new_submission)
                db.session.commit()
                flash('Bestand ingeleverd en aan queue toegevoegd.')
            else:
                flash(f'Filename {fn} impliceert opdracht {cat}. Deze categorie bestaat niet!')

            return redirect(url_for('index'))
        else:
            flash('ERROR: Er ging iets mis. Het bestand is NIET ingeleverd.')
    queued_submissions = current_user.ungraded_submissions().all()

    results = [current_user.best_submission(category) for category in categories]

    return render_template("index.html", title='Home Page', form=form, queued_submissions=queued_submissions, results=results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
