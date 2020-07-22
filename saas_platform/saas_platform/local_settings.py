LANGUAGE_CODE = 'zh-hans'

# 短信配置
APP_ID = 1400399726
APP_KEY = 'f08d9fd061d6d196cf615001f68ddd63'
SMS_SIGN = 'jinsong'

TEMLPATE_ID_DICT = {
    'register': 665398,
    'login': 665398
}

CACHES = {
    'default':{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://49.235.190.157:6379",
        "OPTIONS":{
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS":{
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "p@ssw0rd0"
        }
    }
}