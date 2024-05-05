import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import Flask
from app import db
from app.models import Users, Post


app = Flask(__name__)


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': Users, 'Post': Post}
