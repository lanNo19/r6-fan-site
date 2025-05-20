# run.py

# This file is the entry point for Gunicorn.
# It imports the Flask app instance from your package.

from r6_fan_app import app

if __name__ == '__main__':
    app.run(debug=True)
