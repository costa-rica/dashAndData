import os
import json

if os.environ.get('COMPUTERNAME')=='CAPTAIN2020':
    with open(r'D:\OneDrive\Documents\professional\config_files\config_dashAndData.json') as config_file:
        config = json.load(config_file)
elif os.environ.get('USER')=='sanjose':
    print('computer name is sanjose???')
    with open('/home/sanjose/Documents/environments/config.json') as config_file:
        config = json.load(config_file)
elif os.environ.get('COMPUTERNAME')=='NICKSURFACEPRO4':
    with open(r"C:\Users\Costa Rica\OneDrive\Documents\professional\config_files\config_dashAndData_surface.json") as config_file:
        config = json.load(config_file)
else:
    with open('/home/ubuntu/environments/config.json') as config_file:
        config = json.load(config_file)



class Config:
    DEBUG = True
    MAIL_USE_TLS = True
    SECRET_KEY = config.get('SECRET_KEY_DAD')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    # MAIL_SERVER = config.get('MAIL_SERVER_GOOGLE')
    # MAIL_PORT = config.get('MAIL_SERVER_GOOGLE')
    MAIL_PASSWORD_DAD = config.get('MAIL_PASSWORD_DAD')
    MAIL_USERNAME_DAD = config.get('MAIL_USERNAME_DAD')
    MAIL_SERVER_GD = config.get('MAIL_SERVER_GD')
    MAIL_PORT_GD = config.get('MAIL_PORT_GD')
    # UPLOADED_FILES_FOLDER = os.path.join(os.path.dirname(__file__), 'static/files')
    # UTILITY_FILES_FOLDER = os.path.join(os.path.dirname(__file__), 'static/files_utility')
    # QUERIES_FOLDER = os.path.join(os.path.dirname(__file__), 'static/queries')
    # FILES_DATABASE = os.path.join(os.path.dirname(__file__), 'static/files_database')
    SQLALCHEMY_BINDS ={'dbCage':config.get('SQLALCHEMY_BINDS_DBCAGE'),
        'dbSite' :config.get('SQLALCHEMY_BINDS_DBSITE')}
    GET_STS_FILES = os.path.join(os.path.dirname(__file__), 'static/getSts')
    REGISTRATION_KEY=config.get('REGISTRATION_KEY')
    BLS_API_URL=config.get('BLS_API_URL')
    BLS = os.path.join(os.path.dirname(__file__), 'static/utility_bls')