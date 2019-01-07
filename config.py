import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'twas a cat'

    GOOGLE_CLIENT_ID = '387304838520-akpabffaehou0jegjcnjh7q85jfor2bp.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '7MGjtbm_aM5RMBBeDHUS-cys'
