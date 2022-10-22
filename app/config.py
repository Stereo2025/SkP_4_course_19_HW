class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./HW_19.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JSON_AS_ASCII = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}
#######################################################################################################################
