#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 设置环境变量
export FLASK_ENV=production
export SECRET_KEY="your-secret-key"
export REDIS_HOST="your-redis-host"
export REDIS_PASSWORD="your-redis-password"

# 启动Gunicorn
gunicorn --workers 4 \
         --bind 0.0.0.0:5000 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         --capture-output \
         --log-level info \
         wsgi:application 