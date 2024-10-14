import os
from pathlib import Path
from machina import MACHINA_MAIN_TEMPLATE_DIR, MACHINA_MAIN_STATIC_DIR

# ------- Project Configuration ------------
# Set the base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ------- Security Settings ------------
# WARNING: Keep this secret in production!
SECRET_KEY = 'django-insecure-qm*!z#h%+qxk0z*=y)%0rnnux)jplexkf19y0d%0o#ozp@$a7a'

# Enable debug mode (turn off in production)
DEBUG = True
# DEBUG = False
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ------- User Authentication ------------
# Use a custom user model for authentication
AUTH_USER_MODEL = 'accounts.User'

# ------- Installed Applications ------------
INSTALLED_APPS = [
    # Admin interface enhancements
    'jazzmin',
    'colorfield',


    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # You forget this guys, you'll not makemigrations bruh...
    'django.contrib.humanize',

    # ASGI server
    'channels',
    'django_extensions',
    'chatzone2',


    # Custom apps
    'accounts',
    'mainpage',
    'profiles',

    # Tracking page/Blogging
    'bug',
    'django_summernote',

    # Third-party apps
    'widget_tweaks',
    'django_celery_beat',
    'django_celery_results',
    'corsheaders',
    'rest_framework',
    'django_filters',

    # Learning management system
    'channel',
    'video',
    'channelaccount',


    # Marketplace
    'marketcore',
    'marketchat',
    'marketdash',
    'marketitem',


    # Blog functionality
    'taggit',
    'settings',

    # Rich text editors
    'ckeditor',
    'ckeditor_uploader',
    'tinymce',


    # Forum dependencies
    'mptt',
    'haystack',

    # Machina forum apps
    'machina',
    'machina.apps.forum',
    'machina.apps.forum_conversation',
    'machina.apps.forum_conversation.forum_attachments',
    'machina.apps.forum_conversation.forum_polls',
    'machina.apps.forum_feeds',
    'machina.apps.forum_moderation',
    'machina.apps.forum_search',
    'machina.apps.forum_tracking',
    'machina.apps.forum_member',
    'machina.apps.forum_permission',

    # Security-related apps
    'exploits',
    'crispy_forms',
    'crispy_bootstrap5',

    # Legal and policy
    'terms',


]

# After the INSTALLED_APPS
SITE_ID = 1

# ------- Middleware Configuration ------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Machina forum permissions
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
]

# ------- URL Configuration ------------
ROOT_URLCONF = 'cyberiot.urls'

# ------- Machina Forum Settings -----------
# CKEditor's settings (adjust as needed)
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = 'content/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

MESSAGES_TO_LOAD = 50

# Allow unlimited data upload size (or set to a large value if needed)
DATA_UPLOAD_MAX_MEMORY_SIZE = None  # Or set to a large value like 104857600 (100 MB)

# Optional: Increase file upload size (for image/media uploads)
FILE_UPLOAD_MAX_MEMORY_SIZE = 72428800

PINAX_NOTIFICATIONS_LANGUAGE_MODEL = "app_name.CustomLanguageModel"  # Replace with your actual model
PINAX_NOTIFICATIONS_QUEUE_ALL = False
PINAX_NOTIFICATIONS_HOOKSET = "pinax.notifications.hooks.DefaultHookSet"

# ------- Authentication Configuration ------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Global templates directory
            BASE_DIR / 'marketcore' / 'templates',
            BASE_DIR / 'marketchat' / 'templates',
            BASE_DIR / 'marketdash' / 'templates',
            BASE_DIR / 'marketitem' / 'templates',
            BASE_DIR / 'channel' / 'templates',
            MACHINA_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': True,  # Enables loading templates from app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'machina.core.context_processors.metadata',
            ],
        },
    },
]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'machina_attachments_cache'),  # Updated to an absolute path
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# Channels
ASGI_APPLICATION = 'cyberiot.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_USER_ID = 2  # texting if there's no one, it picks this user
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'channel', 'static'),
    MACHINA_MAIN_STATIC_DIR,

]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# BASE_URL = "http://127.0.0.1:8000"
TEMP = os.path.join(BASE_DIR, 'media/temp')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = 'user:login'
LOGIN_REDIRECT_URL = 'main_page'
LOGOUT_REDIRECT_URL = '/login/'

# Machina settings
# FORUM_NAME = 'CyberIOT'
MARKUP_LANGUAGE = ('machina.core.markdown.markdown', {'safe_mode': True, 'extras': {'break-on-newline': True}})
MARKUP_WIDGET = 'machina.forms.widgets.MarkdownTextareaWidget'
MARKUP_WIDGET_KWARGS = {}
MARKUP_MAX_LENGTH_VALIDATOR = 'machina.core.validators.NullableMaxLengthValidator'
USER_DISPLAY_NAME_METHOD = 'get_username'

FORUM_IMAGE_UPLOAD_TO = 'machina/forum_images'
FORUM_IMAGE_WIDTH = 100
FORUM_IMAGE_HEIGHT = 70

DEFAULT_FORUM_IMAGE_SETTINGS = {
    'width': FORUM_IMAGE_WIDTH,
    'height': FORUM_IMAGE_HEIGHT,
}

FORUM_TOPICS_NUMBER_PER_PAGE = 20

TOPIC_ANSWER_SUBJECT_PREFIX = 'Re:'
POST_CONTENT_MAX_LENGTH = None
TOPIC_POSTS_NUMBER_PER_PAGE = 15
TOPIC_REVIEW_POSTS_NUMBER = 10

POLL_MAX_OPTIONS_PER_POLL = 30
POLL_MAX_OPTIONS_PER_USER = 10

ATTACHMENT_FILE_UPLOAD_TO = 'machina/attachments'
ATTACHMENT_CACHE_NAME = 'machina_attachments'
ATTACHMENT_MAX_FILES_PER_POST = 15

PROFILE_AVATAR_UPLOAD_TO = 'machina/avatar_images'
PROFILE_AVATARS_ENABLED = True
PROFILE_AVATAR_WIDTH = 150
PROFILE_AVATAR_HEIGHT = 250
PROFILE_AVATAR_MIN_WIDTH = None
PROFILE_AVATAR_MAX_WIDTH = None
PROFILE_AVATAR_MIN_HEIGHT = None
PROFILE_AVATAR_MAX_HEIGHT = None
PROFILE_AVATAR_MAX_UPLOAD_SIZE = 0

DEFAULT_AVATAR_SETTINGS = {
    'width': PROFILE_AVATAR_WIDTH,
    'height': PROFILE_AVATAR_HEIGHT,
    'min_width': PROFILE_AVATAR_MIN_WIDTH,
    'max_width': PROFILE_AVATAR_MAX_WIDTH,
    'min_height': PROFILE_AVATAR_MIN_HEIGHT,
    'max_height': PROFILE_AVATAR_MAX_HEIGHT,
    'max_upload_size': PROFILE_AVATAR_MAX_UPLOAD_SIZE,
}

PROFILE_SIGNATURE_MAX_LENGTH = 255
PROFILE_RECENT_POSTS_NUMBER = 15
PROFILE_POSTS_NUMBER_PER_PAGE = 15

DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = []

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# In life, two things define you, your patience when you have nothing and your attitude when you have everything.
