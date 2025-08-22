import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

from models import *

# Explicitly set target_metadata here
# target_metadata = target_db.metadata # This line was added previously
# Let's try to get db from the app context directly for target_metadata
from app import db # Import db from app.py
target_metadata = db.metadata # Set target_metadata directly from db.metadata
