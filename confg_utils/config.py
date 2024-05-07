import os

class Config(Object):
    DEBUG = False # should give us debugging capabilites of every action we take.This should be only true in developement environment.
    CSRF_ENABLED = True # this should protect against Malacious attcks from other sites.
    TESTING = False # this will give us status of our application.if it is True then it says our application is in Testing mode.
    SECRET_KEY = os.getenv("dev_secret_key")   # secret_key is used for saving application and adding flask_app security.
    db_url = "sqlite:///dev.db" # database url
    
    
class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv("dev_secret_key")
    db_url = os.getenv("db_url")
    
class ProductionConfig(Config):
    SECRET_KEY=os.getenv("prod_secret_key")
    db_url = f"postgresql+psycopg2://{os.getenv('SQL_DB_USERNAME')}:{os.getenv('SQL_DB_PASSWORD')}@{os.getenv('SQL_DB_HOST')}/{os.getenv('SQL_DB_NAME')}"