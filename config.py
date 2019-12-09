import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'placeholder')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    GOOGLE_CSE_CX = os.environ.get('GOOGLE_CSE_CX')
    IMAGE_REFRESH_INTERVAL = os.environ.get('IMAGE_REFRESH_INTERVAL', '1000 * 60 * 2')
    TRAP_HTTP_EXCEPTIONS = True
    TEMPLATES_AUTO_RELOAD = True
