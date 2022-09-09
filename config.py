import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLAKCHEMY_COMMIT_ON_TEARDOWN = True
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Mail Settings
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # JWT config
    JWT_SECRET_KEY = "difficult-to-guess-cafe-py"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    USER = os.getenv("POSTGRES_USER_DEV")
    PWD = os.getenv("POSTGRES_PASSWORD_DEV")
    HOSTNAME = os.getenv("POSTGRES_HOSTNAME_DEV")
    PORT = os.getenv("POSTGRES_PORT_DEV")
    DB = os.getenv("POSTGRES_DB_DEV")
    # PROPAGATE_EXCEPTIONS = True  # Prevent expiration exceptions
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PWD}@{HOSTNAME}:{PORT}/{DB}"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    URI = os.getenv("DATABASE_URL")
    if URI and URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = URI.replace(
            "postgres://", "postgresql://", 1)
        SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    USER = os.getenv("POSTGRES_USER_TEST")
    PWD = os.getenv("POSTGRES_PASSWORD_TEST")
    HOSTNAME = os.getenv("POSTGRES_HOSTNAME_TEST")
    PORT = os.getenv("POSTGRES_PORT_TEST")
    DB = os.getenv("POSTGRES_DB_TEST")
    PROPAGATE_EXCEPTIONS = True  # Prevent expiration exceptions
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PWD}@{HOSTNAME}:{PORT}/{DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    PROPAGATE_EXCEPTIONS = True  # Prevent expiration exceptions
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    URI = os.getenv("DATABASE_URL")
    if URI and URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = URI.replace(
            "postgres://", "postgresql://", 1)
        SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
