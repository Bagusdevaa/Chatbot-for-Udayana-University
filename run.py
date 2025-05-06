from app import create_app
from flask import Flask

# Create the Flask application instance
app: Flask = create_app()

if __name__ == '__main__':
    # Run the application with the DEBUG setting from config
    app.run(debug=app.config['DEBUG'])