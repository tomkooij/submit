from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.models import User, Submission
from app.forms import LoginForm, SubmissionForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SubmissionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_submission = Submission('file.py', str(form.comment.data),
                current_user.id)
            db.session.add(new_submission)
            db.session.commit()
            return redirect(url_for('index'))

    queued_submissions = Submission.query.filter_by(user_id=current_user.id, is_graded=False).order_by(Submission.timestamp.desc()).all()

    graded_submissions = Submission.query.filter_by(user_id=current_user.id, is_graded=True).order_by(Submission.timestamp.desc()).all()

    return render_template("index.html", title='Home Page', form=form, queued_submissions=queued_submissions, graded_submissions=graded_submissions)


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = SubmissionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_submission = Submission('file.py', form.comment.data,
                current_user.id)
            db.session.add(new_submission)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('submit.html',
                           form=form)


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
