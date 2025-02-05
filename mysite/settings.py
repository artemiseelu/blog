# 在 MIDDLEWARE 中添加语言中间件
MIDDLEWARE = [
    # ...
    'django.middleware.locale.LocaleMiddleware',
    # ...
]

# 支持的语言
LANGUAGES = [
    ('cn', '中文'),
    ('en', 'English'),
]

# 默认语言
LANGUAGE_CODE = 'cn' 