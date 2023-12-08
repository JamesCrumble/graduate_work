import os

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'OPTIONS': {
            'options': '-c search_path=public,content',
        }
    }
}

if os.environ.get('DEBUG') == 'True':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'formatters': {
            'default': {
                # 'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
                'format': '-=| %(message)s |=-',
            },
        },
        'handlers': {
            'debug-console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'filters': ['require_debug_true'],
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['debug-console'],
                'propagate': False,
            }
        },
    }
