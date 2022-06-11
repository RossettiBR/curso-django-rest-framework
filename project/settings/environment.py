import os
from pathlib import Path
from utils.environment import get_env_variable, parse_comma_sep_str_to_list

BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')


DEBUG = True if os.environ.get('DEBUG') == '1' else False


ALLOWED_HOSTS: list[str] = parse_comma_sep_str_to_list(
    get_env_variable('ALLOWED_HOSTS'))
CSRF_TRUSTED_ORIGINS: list[str] = parse_comma_sep_str_to_list(
    get_env_variable('CSRF_THUSTED_ORIGINS'))

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # noqa: E501
    'PER_SIZE': 10,
}