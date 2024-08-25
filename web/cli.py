import click
from flask import current_app
from flask.cli import with_appcontext
from . import db
@click.command(name='initdb')
@click.option('--drop', is_flag=True, help='Create after drop.')
@with_appcontext
def initdb(drop):
    """Initialize the database."""
    if drop:
       click.echo("Dropping all tables...")
       db.drop_all()
    click.echo('Creating all tables...')
    db.create_all()
    click.echo('Initialized database.')


@click.command(name='admin')
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, help='The password used to login.')
@with_appcontext
def admin(username, password):
    """Create or update an admin user."""
    from .models import User  # 从应用模块中导入 User

    user = User.query.filter_by(username=username).first()
    if user:
        click.echo('Updating user...')
        user.set_password(password)
    else:
        click.echo('Creating new user...')
        user = User(username=username, name=username)
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done.')
