# 生产环境配置
APP_CONFIG = {
    'DEBUG': False,
    'SECRET_KEY': os.environ.get('SECRET_KEY'),  # 从环境变量获取
    'SESSION_TYPE': 'redis',
    'PERMANENT_SESSION_LIFETIME': timedelta(days=7)
}

# Redis配置
DB_CONFIG = {
    'host': os.environ.get('REDIS_HOST', 'localhost'),
    'port': int(os.environ.get('REDIS_PORT', 6379)),
    'password': os.environ.get('REDIS_PASSWORD'),
    'db': 0,
    'decode_responses': True
}

# 安全配置
SECURITY_CONFIG = {
    'ALLOWED_ORIGINS': [
        'https://yourdomain.com',
        'https://www.yourdomain.com'
    ],
    'SSL_REDIRECT': True
} 