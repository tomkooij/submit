import os

from flask import flash, render_template, request, redirect, url_for, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db, pycode
from app.models import User, Submission, categories
from app.forms import LoginForm, SubmissionForm


class AdminModelView(ModelView):

    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        print('callback!!!')
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_admin:
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()


admin = Admin(app, name='submit', index_view=MyAdminIndexView(), template_mode='bootstrap3')

admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Submission, db.session))


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
                flash('Filename {fn} impliceert opdracht {cat}. Deze categorie bestaat niet!'.format(fn=fn, cat=cat))

            return redirect(url_for('index'))
        else:
            flash('ERROR: Er ging iets mis. Het bestand is NIET ingeleverd.')
    queued_submissions = current_user.ungraded_submissions().all()

    results = [current_user.best_submission(category) for category in categories]
    results = [x for x in results if x is not None]

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
