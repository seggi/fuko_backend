import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLAKCHEMY_COMMIT_ON_TEARDOWN = True
    SECURITY_PASSWORD_SALT = 'nankim45'
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Mail Settings
    MAIL_DEFAULT_SENDER = 'seggimarugira@gmail.com'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'seggimarugira@gmail.com'
    MAIL_PASSWORD = 'rapy#2N.'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_DEFAULT_SENDER = 'seggimarugira@gmail.com'
    USER = os.getenv("POSTGRES_USER_DEV")
    PWD = os.getenv("POSTGRES_PASSWORD_DEV")
    HOSTNAME = os.getenv("POSTGRES_HOSTNAME_DEV")
    PORT = os.getenv("POSTGRES_PORT_DEV")
    DB = os.getenv("POSTGRES_DB_DEV")
    PROPAGATE_EXCEPTIONS = True  # Prevent expiration exceptions
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PWD}@{HOSTNAME}:{PORT}/{DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    USER = os.getenv("POSTGRES_USER_TEST")
    PWD = os.getenv("POSTGRES_PASSWORD_TEST")
    HOSTNAME = os.getenv("POSTGRES_HOSTNAME_TEST")
    PORT = os.getenv("POSTGRES_PORT_TEST")
    DB = os.getenv("POSTGRES_DB_TEST")
    PROPAGATE_EXCEPTIONS = True  # Prevent expiration exceptions
    JWT_SECRET_KEY = "difficult-to-guess-cafe-py"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PWD}@{HOSTNAME}:{PORT}/{DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    PROPAGATE_EXCEPTIONS = True  # Prevent expiration exceptions
    MAIL_DEFAULT_SENDER = 'seggimarugira@gmail.com'
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
