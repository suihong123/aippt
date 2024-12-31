from functools import wraps
from flask import request, jsonify
import time
from redis import Redis

class RateLimit:
    def __init__(self, redis_client):
        self.redis = redis_client

    def limit(self, requests=100, window=60):
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                # 获取客户端IP
                client_ip = request.remote_addr
                # 构建Redis键
                key = f'rate_limit:{client_ip}:{request.path}'
                
                # 获取当前时间窗口的请求次数
                current = int(self.redis.get(key) or 0)
                
                if current >= requests:
                    return jsonify({
                        'success': False,
                        'message': '请求过于频繁，请稍后再试'
                    }), 429
                
                # 增加计数器并设置过期时间
                pipe = self.redis.pipeline()
                pipe.incr(key)
                pipe.expire(key, window)
                pipe.execute()
                
                return f(*args, **kwargs)
            return wrapped
        return decorator 