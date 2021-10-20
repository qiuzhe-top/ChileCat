from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'b-u)^cel(1#+=&ian1b2m0e07hr*k8^96fuh*tq+cf^+!!__qd'

DEBUG = True

# 数据类型 1 线上数据库  2 本地Mysql  3 本地Sqlite
DB_TYPE = 1

ENV_PROFILE = os.getenv("ENV")  # 获取环境数值 因为  ENV  只有服务器才配置
if ENV_PROFILE:
    DEBUG = False
    DB_TYPE = 1
    print('线上环境')



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
    'django_extensions',
    'corsheaders',
]

AUTH_USER_MODEL = 'Manage.User'
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


if DB_TYPE == 1:
    USER = 'root'
    HOST = '47.102.215.230'
    DB_NAME = 'ChileCatTest'
elif DB_TYPE == 2:
    USER = 'ChileCatTest'
    HOST = '127.0.0.1'
    DB_NAME = 'ChileCatTest'

if DB_TYPE == 3:
    print('Sqlite 连接中...')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    print('DEBUG:', DEBUG, '数据库:', HOST, DB_NAME)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': USER,
            'PASSWORD': 'zhou24272592',
            'HOST': HOST,
            'PORT': '3306',
            'OPTIONS': {'isolation_level': None},
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

APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# 当访问静态文件时去哪里找
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = ('http://127.0.0.1:8080',)# 允许跨域IP/域名列表
# 跨域允许的请求方式(可选)
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'OPTIONS',
    'DELETE',
    'PATCH',
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
    'EXCEPTION_HANDLER': 'core.rest_permission.exception_handler.custom_exception_handler',
}


DJANGO_COOL = {
    'API_ERROR_CODES': (
        ('ERR_DEMO_NOLOGIN', (3001, '请先登陆')),
        ('ERR_DEMO_PERMISSION', (3002, '权限错误')),
        ('ERR_USER_NOTFOUND', (5001, '用户名或密码错误')),
        ('ERR_USER_NO_PASSWORD', (5007, '密码错误')),
        ('ERR_USER_DIFFERENT_PASSWORD', (5002, '两次密码不一致')),
        ('ERR_USER_DUPLICATE_USERNAME', (5003, '用户名已存在')),
        ('ERR_USER_DUPLICATE_MOBILE', (5004, '手机号已存在')),
        ('ERR_USER_DUPLICATE_EMAIL', (5005, '邮箱已存在')),
        ('ERR_USER_EMAIL_FORMAT_ERROR', (5006, '邮箱格式错误')),
        ('ERR_USER_UNABLE_TO_SEARCH_FOR_USERR', (5008, '搜索的用户不存在')),
        ('ERR_TAKS_USER_HAS_NO_TASK', (5021, '没有对应任务')),
        ('ERR_TASK_ISOPEN_FALSE', (5022, '任务未开启')),
        ('ERR_UPDATE_BADS_IS_NULL', (5023, '床位使用中')),
        ('EXCEL_OUT_NO_DATA', (5024, 'Excel数据为空')),
        ('DORMITORY_NOT_ARRANGED', (5025, '未安排寝室')),
        ('CUSTOM_SCORE_ERROR', (5026, '自定义分数必须在1-10')),
        ('TASK_SUBMISSION_FAILURE', (5027, '任务提交失败')),
        ('THE_REASON_IS_EMPTY', (5028, '原因为空')),
        ('NO_COLLEGE_CODE', (5029, '缺少分院代码/分院不存在')),
    )
}
# SimpleUi 配置
# 服务器信息
SIMPLEUI_HOME_INFO = True
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

# 修改左侧菜单首页设置
# SIMPLEUI_HOME_PAGE = '/api/manage/index'  # 指向页面
# SIMPLEUI_HOME_TITLE = '百度欢迎你!' # 首页标题

# 设置右上角Home图标跳转链接，会以另外一个窗口打开
SIMPLEUI_INDEX = 'http://www.qiuzhe.top'
