from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
            return check_password_hash(self.password_hash, password)

    def ungraded_submissions(self):
        return Submission.query.filter_by(user_id=self.id, is_graded=False).order_by(Submission.timestamp.desc())

    def graded_submissions(self):
        return Submission.query.filter_by(user_id=self.id, is_graded=True).order_by(Submission.timestamp.desc())

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_filename = db.Column(db.String, default=None, nullable=True)
    stored_filename = db.Column(db.String, default=None, nullable=True)
    comment = db.Column(db.String(140))
    is_graded = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=-1)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, filename, comment, user_id):
        self.submission_filename = filename
        self.comment = comment
        self.user_id = user_id

    def set_grade(self, score):
        self.score = score
        self.is_graded = True

    def __repr__(self):
        return '<Submission {} {} {}>'.format(self.submission_filename, self.timestamp, self.is_graded)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
