from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .doctor import Doctor
from .appointment import Appointment


