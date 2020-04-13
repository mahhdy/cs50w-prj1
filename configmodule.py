class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgres://jjftsdutfuwhhl:c773f8e072b7c4cbc5736ecc10b042961c11d0efe8a7b54aecfca685be041851@ec2-18-235-20-228.compute-1.amazonaws.com:5432/dbb5crinco6nc9'
    SECRET_KEY = "utfuwhhl:c773ILoveYou!42961c11d0ef"
    SESSION_PERMANENT=False
    SESSION_TYPE="filesystem"
    
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV='development'

class TestingConfig(Config):
    DEBUG = True