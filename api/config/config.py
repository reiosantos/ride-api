"""
Config file contains global CONSTANTS
"""
from api.utils.utils import JSONSerializable


class HostConfig:
    """
    System HOST configuration settings
    They can be changed at any time.
    """
    HOST = "0.0.0.0"
    PORT = 5000


class ServerConfig(JSONSerializable):
    """
    System configuration settings
    They can be changed at any time.
    """

    SECRET_KEY = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
    SECURITY_PASSWORD_SALT = 'efa27950565790fbaecfb5fb64b84a6a7c48d06d'


class EnvironmentConfig(ServerConfig):
    """
    System configuration settings for running environment
    They can be changed at any time.
    It extends the server congig class
    """
    DEBUG = True
    TESTING = False
    ENV = "development"


class DatabaseConfig:
    """
    System configuration settings for running environment
    They can be changed at any time.
    It extends the server congig class
    """
    HOST = "ec2-54-227-244-122.compute-1.amazonaws.com"  # "127.0.0.1"
    PORT = "5432"
    DATABASE = "dfvbqjpifjouqa"  # "ride-api"

    SCHEMA_PRODUCTION = "production"
    SCHEMA_TESTING = "tests"
    USER = "djtuplqlttpocs"  # "postgres"
    PASSWORD = "480588ba2a7bf853d251f2fe57e94bbfa3168f720ed46ee798edf55075f6693d"  # "santos"
