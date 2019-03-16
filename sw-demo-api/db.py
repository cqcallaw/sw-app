import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import orm

def get_engine():
    if 'engine' not in g:
        engine = create_engine('sqlite:///' + current_app.config['DATABASE'], echo=True)
        g.engine = engine

    return g.engine

def get_session_maker():
    if 'session_maker' not in g:
        engine = get_engine()
        session_maker = sessionmaker(bind=engine)
        g.session_maker = session_maker

    return g.session_maker

def close_db(e=None):
    pass

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db_path = current_app.config['DATABASE']
    # purge existing data, for demo purposes
    if os.path.exists(db_path):
        os.remove(db_path)
    orm.init_db(db_path, get_engine(), get_session_maker())
    click.echo('Initialized the database.')
