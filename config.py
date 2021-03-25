class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    ENV = "prod"
    IMAGE_UPLOADS = "./upload/images"
    UPLOAD_EXTENSIONS_IMAGES = ['.jpg', '.png', '.gif']

    MEDIA_UPLOADS = "./upload/media"
    UPLOAD_EXTENSIONS_MEDIA = ['.webm']


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "dev"
    
class TestingConfig(Config):
    TESTING = True
    ENV = "testing"
    SESSION_COOKIE_SECURE = False