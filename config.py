import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'placeholder')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    GOOGLE_CSE_CX = os.environ.get('GOOGLE_CSE_CX')
    EFFECT_COUNT = 3
    NOUN_COUNT = 2
    TRAP_HTTP_EXCEPTIONS = True
    TEMPLATES_AUTO_RELOAD = True
