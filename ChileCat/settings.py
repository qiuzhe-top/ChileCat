from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'b-u)^cel(1#+=&ian1b2m0e07hr*k8^96fuh*tq+cf^+!!__qd'

# 获取环境数值 因为  ENV  只有服务器才配置
ENV_PROFILE = os.getenv("ENV")

DEBUG = True
HOST = '127.0.0.1'

if ENV_PROFILE:
    HOST = '47.102.215.230'
    DEBUG = False

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'cool',
    'Apps.User',
    'Apps.SchoolInformation',
    'Apps.SchoolAttendance',
    'Manage',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 跨域
    'django.middleware.common.CommonMiddleware',  # 跨域
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'Manage.utils.middleware.LoadUserObject',
]

ROOT_URLCONF = 'ChileCat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'Manage.utils.context_processors.get_permissions',
            ],
        },
    },
]

WSGI_APPLICATION = 'ChileCat.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

print('DEBUG:', DEBUG, '数据库:', HOST)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ChileCat',
        'USER': 'root',
        'PASSWORD': 'zhou24272592',
        'HOST': HOST,
        'PORT': '3306',
        'OPTIONS': {'isolation_level': None},
    }
}

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'


# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = ('*')#跨域增加忽略
# 跨域允许的请求方式(可选)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
# 跨域允许的头部参数(可选)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'access-control-allow-origin',
    'Access-Control-Allow-Origin',
    'token',
)

# JWT 密钥
SECRET_KEY = 'AHABsyAS.ASD.?SA&&w1dsa.1.sdssagrh.;ASLKI'

# 全局权限控制
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "core.rest_permission.authentication.AuthPermission",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "core.rest_permission.api_permission.ApiPublicPermission",
    ],
    'EXCEPTION_HANDLER': 'core.rest_permission.exception_handler.custom_exception_handler',
}


DJANGO_COOL = {
    'API_ERROR_CODES': (
        ('ERR_PER_NOLOGIN', (3001, '请先登陆')),
        ('ERR_PER_PERMISSION', (3002, '权限错误')),
        ('ERR_USER_NOTFOUND', (5001, '用户名或密码错误')),
        ('ERR_USER_NO_PASSWORD', (5007, '密码错误')),
        ('ERR_USER_DIFFERENT_PASSWORD', (5002, '两次密码不一致')),
        ('ERR_USER_DUPLICATE_USERNAME', (5003, '用户名已存在')),
        ('ERR_USER_DUPLICATE_MOBILE', (5004, '手机号已存在')),
        ('ERR_USER_DUPLICATE_EMAIL', (5005, '邮箱已存在')),
        ('ERR_USER_EMAIL_FORMAT_ERROR', (5006, '邮箱格式错误')),
    )
}
