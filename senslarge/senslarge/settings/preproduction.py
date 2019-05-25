# import os

# import raven

# from .base import *  # noqa


# DEBUG = False

# ALLOWED_HOSTS = ['senslarge.hashbang.fr']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'senslarge',
#         'USER': 'senslarge',
#     }
# }

# STATIC_ROOT = '/srv/app/senslarge/static/'
# MEDIA_ROOT = '/srv/app/senslarge/media/'

# INSTALLED_APPS += [  # noqa
#     'raven.contrib.django.raven_compat',
# ]

# RAVEN_CONFIG = {
#     'dsn': 'https://27e44805b758497f82409820824b24b4:'
#            'aba8b4ab78e749108b38038e6dff3f92@sentry.hashbang.fr/28',
#     'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
# }

# MIDDLEWARE = [
#     'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
# ] + MIDDLEWARE  # noqa


# DEFAULT_FROM_EMAIL = 'evaluations@senslarge.hashbang.fr'

# WEASYPRINT_BASEURL = 'https://senslarge.hashbang.fr'

# EMAIL_HOST_USER = 'postmaster@senslarge.hashbang.fr'
# EMAIL_HOST_PASSWORD = '9d38fd2cb447d06ef87b068eb2c5aad2'
