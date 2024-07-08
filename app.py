import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import Flask
from app import db
from app.models import User, Post


app = Flask(__name__)