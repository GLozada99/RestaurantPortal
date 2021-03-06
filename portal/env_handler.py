from decouple import UndefinedValueError, config


class EnvHandler:
    """Class to handle environment variables."""

    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', default=False, cast=bool)
    ALLOWED_HOSTS = config('ALLOWED_HOSTS').strip().split()
    EXPIRATION_DELTA = config('EXPIRATION_DELTA', default=15, cast=int)
    AUTH_HEADER_PREFIX = config('AUTH_HEADER_PREFIX', default='Bearer')
    LOGS_FILE = config('LOGS_FILE', default='app') + '.log'
    DJANGO_SETTINGS_MODULE = config('DJANGO_SETTINGS_MODULE')

    AWS_S3_ACCESS_KEY_ID = config('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = config('AWS_S3_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_QUERYSTRING_AUTH = config('AWS_QUERYSTRING_AUTH', cast=bool)
    GOOGLE_ID = config('GOOGLE_ID')

    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
    EMAIL_PORT = config('EMAIL_PORT', cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_PASSWORD_CHANGE_LINK = config('EMAIL_PASSWORD_CHANGE_LINK')

    def __init__(self):
        try:
            db_name = config('DB_NAME')
            db_user = config('DB_USER')
            db_pass = config('DB_PASSWORD')
            db_host = config('DB_HOST')
            db_port = config('DB_PORT')
            self.DB_URL = (
                f'postgresql://'
                f'{db_user}:'
                f'{db_pass}@'
                f'{db_host}:'
                f'{db_port}/'
                f'{db_name}'
            )
        except UndefinedValueError:
            self.DB_URL = config('DATABASE_URL')
