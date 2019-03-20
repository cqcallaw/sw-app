""" App controllers """
import flask
from flask_login import current_user, login_user, login_required
from auth_demo.models import User
from auth_demo.extensions import LOGIN_MANAGER
from auth_demo.forms import LoginForm

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
    return flask.render_template('index.html')

def login_handler():
    """ Handle user login """
    form = LoginForm()
    if form.validate_on_submit():
        login_user(current_user)

        flask.flash('Logged in successfully.')

        redirect_url = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(redirect_url):
            return flask.abort(400)

        return flask.redirect(redirect_url or flask.url_for('base_handler'))

    return flask.render_template('login.html', form=form)

def logout_handler():
    """ Logout handler """

def register_handler():
    """ Register handler """

@login_required
def users_handler():
    """ Users view handler """

@login_required
def user_handler():
    """ User view handler """

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """ Load user interface """
    try:
        return User.query.get(user_id)
    except:  # pylint: disable=bare-except
        return None

def is_safe_url(redirect_url):
    """ Check for safe URL redirect """
    return True
