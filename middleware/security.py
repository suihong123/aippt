from functools import wraps
from flask import request, abort
import re

class SecurityMiddleware:
    def __init__(self):
        # XSS 攻击特征
        self.xss_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'onerror=',
            r'onload='
        ]
        
        # SQL 注入特征
        self.sql_patterns = [
            r'UNION.*SELECT',
            r'DROP.*TABLE',
            r'DELETE.*FROM',
            r'INSERT.*INTO',
            r'--',
            r';'
        ]

    def check_security(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # 检查请求头
            if not self._check_headers():
                abort(400)
            
            # 检查请求参数
            if not self._check_parameters():
                abort(400)
            
            return f(*args, **kwargs)
        return wrapped

    def _check_headers(self):
        """检查请求头"""
        # 检查 Content-Type
        if request.method == 'POST':
            content_type = request.headers.get('Content-Type', '')
            if not content_type.startswith(('application/json', 'multipart/form-data')):
                return False
        
        # 检查 Origin
        origin = request.headers.get('Origin')
        if origin and origin not in ['http://localhost:5000', 'https://yourdomain.com']:
            return False
        
        return True

    def _check_parameters(self):
        """检查请求参数"""
        for key, value in request.values.items():
            # 检查 XSS
            for pattern in self.xss_patterns:
                if re.search(pattern, str(value), re.I):
                    return False
            
            # 检查 SQL 注入
            for pattern in self.sql_patterns:
                if re.search(pattern, str(value), re.I):
                    return False
        
        return True 