#配置文件

class  BaseConfig(object):
    SECRET_KEY = 'secret string'
    MONGO_URI = 'mongodb://localhost:27017/test'

class DevelopmentConfig(BaseConfig):
    MONGO_URI = 'mongodb://test:test@localhost/test'

class ProductionConfig(BaseConfig):
    MONGO_URI = 'mongodb://admin:123456@localhost/admin'

config = {

        'development':DevelopmentConfig,
        'production':ProductionConfig
        }


