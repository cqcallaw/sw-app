""" App controllers """
from urllib.parse import urlparse, urljoin
import flask
from flask_login import login_user, logout_user, login_required
from auth_demo.models import User
from auth_demo.extensions import LOGIN_MANAGER, BCRYPT_HANDLE
from auth_demo.forms import LoginForm

def init(app):
    """ Init app controllers """
    with app.app_context():
        app.add_url_rule('/', view_func=base, methods=['GET'])
        app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
        app.add_url_rule('/logout', view_func=logout, methods=['GET'])
        app.add_url_rule('/register', view_func=register, methods=['GET'])
        app.add_url_rule('/users', view_func=users, methods=['GET'])
        app.add_url_rule('/users<string:user_id>', view_func=user, methods=['GET'])
        app.add_url_rule('/register', view_func=register, methods=['GET'])

def base():
    """ Base URL handler """
    return flask.render_template('index.html')

def login():
    """ Handle user login """
    form = LoginForm()
    if form.validate_on_submit():
        user_id = flask.request.form['user_id']
        password = flask.request.form['password']

        subject = User.query.get(user_id)

        if not subject:
            return flask.render_template('login.html', form=form, error='unknown user')

        if not BCRYPT_HANDLE.check_password_hash(subject.password, password):
            return flask.render_template('login.html', form=form, error='invalid password')

        login_user(subject)

        redirect_url = flask.request.args.get('next')
        if not is_safe_url(redirect_url):
            return flask.abort(400)

        return flask.redirect(redirect_url or flask.url_for('base'))

    return flask.render_template('login.html', form=form)

def logout():
    """ Logout handler """
    logout_user()
    return flask.redirect(flask.url_for('base'))

def register():
    """ Register handler """

@login_required
def users():
    """ Users view handler """

@login_required
def user():
    """ User view handler """

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """ Load user interface """
    try:
        return User.query.get(user_id)
    except:  # pylint: disable=bare-except
        return None

def is_safe_url(target):
    """ Check for safe URL redirect """
    # ref: http://flask.pocoo.org/snippets/62/
    ref_url = urlparse(flask.request.host_url)
    test_url = urlparse(urljoin(flask.request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
