from flask import flash, render_template, request, redirect, url_for, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import UploadNotAllowed

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db, pycode
from app.models import User, Submission, categories
from app.forms import LoginForm, SubmissionForm


def best_submissions(user):
    """return a list of the best submissions per category for a user"""
    results = [user.best_submission(category) for category in categories]
    return [x for x in results if x is not None]


def total_score(user):
    """returns the total score (cijfer?) for a user"""
    scores = [user.best_score(category) for category in categories]
    return sum(scores)


@app.route('/show/<path:path>')
@login_required
def show_file(path):
    # make sure the file belongs to the current user
    # the query will throw a 404 if file does not exists for the current user
    Submission.query.filter_by(submission_filename=path, user_id=current_user.id).first_or_404()
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


@app.route('/sub/<id>')
@login_required
def sub_page(id):
    submission = Submission.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('submission.html', submission=submission)


@app.route('/results/<category>')
@login_required
def results_page(category):
    submissions = Submission.query.filter_by(category=category, user_id=current_user.id, is_graded=True).all()
    result = current_user.best_submission(category)
    return render_template('results.html', result=result, submissions=submissions)


@app.route('/all_results')
@login_required
def all_results_page():
    if not current_user.is_admin:
        return redirect(url_for('login'))
    users = User.query.all()
    stats = {}
    for user in users:
        stats[user] = best_submissions(user)
    return render_template('all_results.html', stats=stats)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SubmissionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            fn = form.submission_file.data.filename
            try:
              filename = pycode.save(form.submission_file.data, folder=secure_filename(current_user.username))
            except UploadNotAllowed:
              flash('Alleen .py en .ipynb toegestaan. Het bestand is NIET ingeleverd.')
              return redirect(url_for('index'))
            new_submission = Submission(filename=filename, comment=str(form.comment.data), user_id=current_user.id, category=form.submission_category.data)
            db.session.add(new_submission)
            db.session.commit()
            flash('Bestand ingeleverd en aan queue toegevoegd.')

            return redirect(url_for('index'))
        else:
            flash('ERROR: Er ging iets mis. Het bestand is NIET ingeleverd.')
    queued_submissions = current_user.ungraded_submissions().all()

    results = best_submissions(current_user)
    score = total_score(current_user)

    return render_template("index.html", title='Home Page', form=form, queued_submissions=queued_submissions, results=results, score=score)


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
