# config.py

import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'wyhjmmxmjhhdytd'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    JSON_COMPACT = False
