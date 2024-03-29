import os

from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config['secret_key'] = "clive69"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'clivefernandes20@gmail.com'  # Your Gmail email address
    app.config['MAIL_PASSWORD'] = 'weww gpah mqdb jfax'  # Your Gmail password or app-specific password
    app.config['MAIL_DEFAULT_SENDER'] = 'clivefernandes20@gmail.com'  # Your Gmail email address

    if test_config:
        app.config.from_mapping(test_config)

    return app