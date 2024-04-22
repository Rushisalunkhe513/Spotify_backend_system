class Config:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration class"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class ProductionConfig(Config):
    """Production configuration class"""
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/db_name'

# Other configurations can be added for testing, staging, etc.

# Function to select configuration based on environment
def get_config(env):
    if env == 'development':
        return DevelopmentConfig
    elif env == 'production':
        return ProductionConfig
    else:
        raise ValueError("Invalid environment")

# Usage example
import os

# Set FLASK_ENV environment variable to 'development' or 'production'
env = os.environ.get('FLASK_ENV', 'development')

# Get the configuration based on the environment
config = get_config(env)
