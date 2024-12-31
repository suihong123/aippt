import time
from functools import wraps
from flask import request, g
import psutil
import logging

class PerformanceMonitor:
    def __init__(self):
        self.logger = logging.getLogger('performance')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('performance.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)

    def monitor(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # 记录请求开始
            g.start_time = start_time
            
            result = f(*args, **kwargs)
            
            # 计算性能指标
            duration = time.time() - start_time
            memory_used = psutil.Process().memory_info().rss / 1024 / 1024 - start_memory
            
            # 记录性能日志
            self.logger.info({
                'path': request.path,
                'method': request.method,
                'duration': f'{duration:.3f}s',
                'memory_used': f'{memory_used:.2f}MB',
                'status_code': getattr(result, 'status_code', 200)
            })
            
            return result
        return wrapped

    def get_system_stats(self):
        """获取系统状态"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent
        } 