import os
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # noqa: E501
    'PER_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT-RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'BLACKLIST_AFTER_ROTATION': False,
    'SIGNING_KEY': os.environ.get('SECRET_KEY_JWT', 'INSECURE'),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
