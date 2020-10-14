# -*- coding: utf-8 -*-
class Config:
    """
        Class to define the type of environment configutation
        * class      Config, DevelopmentConfig, TestingConfig, ProductionConfig
        * requires   python 3.7
        * version    1.0.0
        * developer  Alcindo Schleder <alcindo.schleder@amcom.com.br>
    """

    SECRET_KEY = None
    HOST_SERVER = '0.0.0.0'
    SERVER_PORT = 5000
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    HOST_SERVER = '127.0.0.1'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    HOST_SERVER = '127.0.0.1'


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
