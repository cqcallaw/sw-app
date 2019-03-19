""" App controllers """
import flask
from flask_login import login_user, render_template
from auth_demo.models import User
from auth_demo.extensions import LOGIN_MANAGER

def init(app):
    """ Init app controllers """
    with app.app_context():
        app.add_url_rule('/', view_func=base_handler, methods=['GET'])
        app.add_url_rule('/login', view_func=login_handler, methods=['GET', 'POST'])
        app.add_url_rule('/logout', view_func=logout_handler, methods=['GET'])
        app.add_url_rule('/register', view_func=register_handler, methods=['GET'])
        app.add_url_rule('/users', view_func=users_handler, methods=['GET'])
        app.add_url_rule('/users<string:user_id>', view_func=user_handler, methods=['GET'])
        app.add_url_rule('/register', view_func=register_handler, methods=['GET'])

def base_handler():
    """ Base URL handler """
    return render_template('index.html')

def login_handler():
    """ Handle user login """
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        redirect_url = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(redirect_url):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

def logout_handler():
    """ Logout handler """

def register_handler():
    """ Register handler """

def users_handler():
    """ Users view handler """

def user_handler():
    """ User view handler """

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """ Load user interface """
    return User.query.filter_by(user_id=user_id).first()

def is_safe_url(redirect_url):
    """ Check for safe URL redirect """
    return True
