from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask_mail import Mail
from dashAndData.config import Config
# from flask_migrate import Migrate

# import logging
import sys

db = SQLAlchemy()

# bcrypt = Bcrypt()
# login_manager= LoginManager()
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
# mail = Mail()

#application factory
def create_app(config_class=Config):
    app = Flask(__name__)
    
    # logger = logging.getLogger(__name__)
    # stderr_handler = logging.StreamHandler(sys.stderr)
    # logger.addHandler(stderr_handler)
    # file_handler = logging.FileHandler('dashAndData_log.txt')
    # file_handler.setLevel(logging.DEBUG)
    # logger.addHandler(file_handler)
    # app.logger.addHandler(file_handler)
    
    app.config.from_object(Config)

    db.init_app(app)
    # bcrypt.init_app(app)
    # login_manager.init_app(app)
    # mail.init_app(app)

    
    from dashAndData.blog.routes import blog
    from dashAndData.datatools.routes import datatools
    from dashAndData.main.routes import main
    # from dashAndData.errors.handlers import errors
    from dashAndData.datatools.cage_search.routes import datatools_cage
    
    
    app.register_blueprint(blog)
    app.register_blueprint(datatools)
    app.register_blueprint(main)
    # app.register_blueprint(errors)
    app.register_blueprint(datatools_cage)

    return app