from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for

from app import app, db
from app.models import User, Submission


class AdminModelView(ModelView):

    def is_accessible(self):
        """only users with is.admin=True should have access to admin
        panel. However, if they somehow get access, block these models
        anyway. Users will get empty admin panel.
        """
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        """redirect to login page if user doesn't have access"""
        return redirect(url_for('login', next=request.url))


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        """only allow admin, redirect others"""
        if not current_user.is_admin:
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()


admin = Admin(app, name='submit', index_view=MyAdminIndexView(), template_mode='bootstrap3')

admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Submission, db.session))
