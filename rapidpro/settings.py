import os
import warnings

from temba.settings_common import *  # noqa


def get_env_as_list(key, default=None):
    return [
        o.strip() for o in os.getenv(key, default).split(",")
    ]


DEBUG = os.getenv("DEBUG", "no") == "yes"

if DEBUG:
    MIDDLEWARE = ("temba.middleware.ExceptionMiddleware",) + MIDDLEWARE

# -----------------------------------------------------------------------------------
# This setting throws an exception if a naive datetime is used anywhere. (they should
# always contain a timezone)
# -----------------------------------------------------------------------------------
warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)

ALLOWED_HOSTS = get_env_as_list("ALLOWED_HOSTS", "")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL", "http://minio:9000")
STORAGE_URL = f"{AWS_S3_ENDPOINT_URL}/{BUCKET_PREFIX}-default"
DYNAMO_ENDPOINT_URL = os.getenv("DYNAMO_ENDPOINT_URL", "http://dynamo:6000")
DYNAMO_TABLE_PREFIX = os.getenv("DYNAMO_TABLE_PREFIX", "Temba")
ELASTIC_ENDPOINT_URL = os.getenv("ELASTIC_ENDPOINT_URL", "http://elastic:9200")
CSRF_TRUSTED_ORIGINS = get_env_as_list("CSRF_TRUSTED_ORIGINS", "")
_db = {
    "ATOMIC_REQUESTS": True,
    "CONN_MAX_AGE": 60,
    "DISABLE_SERVER_SIDE_CURSORS": True,
    "ENGINE": "django.contrib.gis.db.backends.postgis",
    "HOST": os.getenv("DB_HOST", "postgres"),
    "NAME": os.getenv("DB_NAME", "temba"),
    "OPTIONS": {},
    "PASSWORD": os.getenv("DB_PASSWORD", ""),
    "PORT": os.getenv("DB_PORT", "5432"),
    "USER": os.getenv("DB_USER", "temba"),
}
DATABASES = {"default": _db, "readonly": _db.copy()}
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_DEFAULT_FROM")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT", "25")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "yes") == "yes"
EMAIL_HOST_USER = os.getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
FLOW_FROM_EMAIL = os.getenv("EMAIL_FLOW_FROM")
HOSTNAME = os.getenv("HOSTNAME", "localhost")
# same 32 hex character format as mailroom, split into four 32-bit integers
_id_key = os.getenv("ID_OBFUSCATION_KEY")
if _id_key:
    ID_OBFUSCATION_KEY = tuple(int(_id_key[i : i + 8], 16) for i in range(0, 32, 8))
INTERNAL_IPS = ("127.0.0.1",)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"level": "INFO", "handlers": ["console"]},
        "django.request": {"level": "ERROR", "handlers": ["console"]},
        "idems": {"level": "INFO", "handlers": ["console"]},
        "temba": {"level": "INFO", "handlers": ["console"]},
    },
}
MAILROOM_URL = os.getenv("MAILROOM_URL", "http://mailroom:8090")
MAILROOM_AUTH_TOKEN = os.getenv("MAILROOM_AUTH_TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
STATIC_URL = "/static/"
BRAND["domain"] = os.getenv("BRAND_DOMAIN")
BRAND["emails"]["notifications"] = os.getenv("BRAND_EMAILS_NOTIFICATIONS")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
IDEMS_EXPORT_BASE_URL = f"https://{BRAND['domain']}/idems/export"
MIDDLEWARE += ("idems.middleware.ExportDownloadMiddleware",)
