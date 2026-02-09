import click
from app import db
from app.models import User

def register_commands(app):
    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("password")
    def create_admin(username, password):
        """Creates a new admin user."""
        if User.query.filter_by(username=username).first():
            print(f"User '{username}' already exists.")
            return
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

    @app.cli.command("init-db-data")
    def init_db_data():
        """Creates the default admin user."""
        if User.query.filter_by(username='admin').first():
            print("Default admin user already exists.")
        else:
            user = User(username='admin')
            user.set_password('123456')
            db.session.add(user)
            db.session.commit()
            print("Default admin user 'admin' created successfully.")
