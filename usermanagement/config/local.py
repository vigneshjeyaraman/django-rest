DATABASES = {
    'default': {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': 'usermanagement',
    'USER':'tushar',
    'PASSWORD':'tushar',
    'HOST':'localhost',
    # 'PORT': '5433'
}
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
    'pagination.Pagination',
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication', 
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',),
    'EXCEPTION_HANDLER': 'custom_exception.common_exception.custom_exception_handler',
}

SEND_GRID_API_KEY = ''
FROM_EMAIL = "support@mail.com"