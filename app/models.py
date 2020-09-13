from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

# this could be a table...
categories = ['nulputen', 'plot', 'riemann', 'rekenwonder', 'fit',
            'fuzzymatches', 'countmatches', 'goldbach', 'tunnel',
            'piramide', 'randomwiskunde', 'levenshtein', 'greedy',
            'priemgetal', 'water', 'temperatuur', 'monopoly', 'initials',
            'autorit', 'histogram', 'hello', 'basejump', 'montecarlo',
            'appel', 'reeks', 'findmatches', 'afstand',
            'monopoly_realistisch', 'nulpunten']


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    naam = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
            return check_password_hash(self.password_hash, password)

    def ungraded_submissions(self):
        return Submission.query.filter_by(user_id=self.id, is_graded=False).order_by(Submission.timestamp.desc())

    def graded_submissions(self):
        return Submission.query.filter_by(user_id=self.id, is_graded=True).order_by(Submission.timestamp.desc())

    def best_submission(self, category):
        return Submission.query.filter_by(user_id=self.id, category=category, is_graded=True).order_by(Submission.score.desc()).first()

    def __init__(self, username=None, naam=None, email=None):
        assert username is not None
        self.username = username
        self.naam = naam
        self.email = email

    def __repr__(self):
        return '<User #{}, username: {} "{}">'.format(self.id, self.username, self.naam)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_filename = db.Column(db.String(30), default=None, nullable=True)
    stored_filename = db.Column(db.String(100), default=None, nullable=True)
    comment = db.Column(db.String(140))
    category = db.Column(db.String(30), default=None, nullable=True)
    is_graded = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=-1)
    nTests = db.Column(db.Integer, default=-1)
    nPassed = db.Column(db.Integer, default=-1)
    checkpy_output = db.Column(db.String(1000), default=None, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, filename=None, comment=None, user_id=None, category=categories[0]):
        self.submission_filename = filename
        self.comment = comment
        self.user_id = user_id
        self.category = category

    def set_grade(self, score):
        self.score = score
        self.is_graded = True

    def __repr__(self):
        return '<Submission #{}: {} {} {} {}>'.format(self.id, self.submission_filename, self.timestamp, self.is_graded, self.score)
