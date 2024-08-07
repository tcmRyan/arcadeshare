"""
Custom view to integrate flask-admin with the authentication and
authorization of flask-security
"""
from flask import abort, redirect
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, url_for_security
from wtforms import StringField


class UserView(ModelView):
    ignore_hidden = False
    column_hide_backrefs = False
    column_list = ('email', 'active', 'roles', 'password')
    form_columns = ("email", "username", "active", "roles", "password", "tenant")
    form_excluded_columns = ('oauth',)
    form_extra_fields = {
        "password": StringField("password")
    }


class ArcadeAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role("superadmin"):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when the view is not accessible
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # Permission Denied
                abort(403)
            else:
                # login
                return redirect(url_for_security("login", next="/admin"))
