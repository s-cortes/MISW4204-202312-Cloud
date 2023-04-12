class ProductionConfig(object):
    TESTING = False
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = True

class DevelopmentConfig(ProductionConfig):
    TESTING = True
    DEBUG = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = False

ENV_CONFIG = {
    0: 'config.ProductionConfig',
    1: 'config.DevelopmentConfig',
}
