# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LOCALE_PATHS = ['movies/locale']

LANGUAGE_CODE = 'ru'
# LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
