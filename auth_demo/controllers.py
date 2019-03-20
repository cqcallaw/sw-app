""" App controllers """
from urllib.parse import urlparse, urljoin
import flask
from flask_login import login_required
from auth_demo.models import User
from auth_demo.extensions import LOGIN_MANAGER
from auth_demo.forms import LoginForm, RegistrationForm

def init(app):
    """ Init app controllers """
    with app.app_context():
        app.add_url_rule('/', view_func=base, methods=['GET'])
        app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
        app.add_url_rule('/register', view_func=register, methods=['GET'])
        app.add_url_rule('/users', view_func=users, methods=['GET'])
        app.add_url_rule('/users/<string:user_id>', view_func=user, methods=['GET'])
        app.add_url_rule('/register', view_func=register, methods=['GET'])

def base():
    """ Base URL handler """
    return flask.render_template('index.html')

def login():
    """ Handle user login """
    form = LoginForm()
    return flask.render_template('login.html', form=form)

def register():
    """ Register handler """
    form = RegistrationForm()
    return flask.render_template('register.html', form=form)

@login_required
def users():
    """ Users view handler """
    return flask.redirect(flask.url_for('base'))

@login_required
def user(user_id):
    """ User view handler """
    user_definition = User.query.get(user_id)

    if not user_definition:
        return 'User %s not found' % user_id, 404

    return flask.render_template('user.html', user_definition=user_definition)

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
