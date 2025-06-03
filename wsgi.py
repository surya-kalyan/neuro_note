# This file is intended for use with WSGI servers like Gunicorn.
# It imports the Flask application instance from neuronote.py.

from neuronote import app # Assuming your Flask app instance is named 'app' in neuronote.py
from utils.logger import logger # Optional: if you want to log WSGI server related info

# The WSGI server will look for the 'app' object in this file.
# Example Gunicorn command: gunicorn --bind 0.0.0.0:5000 wsgi:app

# No __main__ block is typically needed here for Gunicorn.
# neuronote.py's __main__ block handles development server execution.
# If this file is executed directly, it won't do anything by itself unless
# the app import itself triggers actions (which it shouldn't in a well-structured app).

logger.info("wsgi.py loaded. Flask 'app' object is now available for WSGI server.")
